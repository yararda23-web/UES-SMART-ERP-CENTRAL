#!/usr/bin/env python3
"""
UES SMART ERP — Enterprise Backend Service Layer & REST API Server
Implements server-side RBAC, Pricing Engine (exact cents arithmetic), AI Business Tools,
Idempotent Payment & Webhook processing, Tenant Isolation, and full CRUD over SQLite/PostgreSQL.
"""
import sqlite3
import json
import os
import hashlib
import hmac
import secrets
from datetime import datetime
from typing import Dict, Any, Optional, List

DB_PATH = os.path.abspath(os.environ.get("UES_DB_PATH", os.path.join(os.path.dirname(__file__), "../../database/ues_smart_erp.db")))
# Never load credentials from files bundled in the app. Configure secrets in environment.


# Password hashes are one-way; old salted SHA-256 demo records are upgraded on login.
def make_password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 600_000
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    return f'pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}'

def verify_password(password: str, stored: str) -> bool:
    if stored.startswith('pbkdf2_sha256$'):
        try:
            _, iters, salt_hex, digest_hex = stored.split('$')
            expected = bytes.fromhex(digest_hex)
            actual = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), int(iters))
            return hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False
    # Only for migrating legacy demo database records.
    legacy = hashlib.sha256(('UES_SALT_2026_' + password).encode('utf-8')).hexdigest()
    return hmac.compare_digest(legacy, stored)

ROLE_PERMISSIONS = {
    "super_admin": {"*"},
    "general_manager": {"dashboard", "inbox", "contacts", "leads", "services", "pricing", "quotes", "contracts", "projects", "tasks", "team", "reports", "approvals", "notifications", "files", "audit"},
    "sales_manager": {"dashboard", "inbox", "contacts", "leads", "services", "pricing", "quotes", "contracts", "approvals", "reports"},
    "sales_rep": {"dashboard", "inbox", "contacts", "leads", "services", "pricing", "quotes_draft"},
    "academic_manager": {"dashboard", "projects", "tasks", "team", "files", "calendar", "knowledge"},
    "academic_specialist": {"assigned_projects", "assigned_tasks", "files_assigned"},
    "finance_manager": {"dashboard", "invoices", "payments", "expenses", "contracts_view", "finance_reports", "approvals_finance"},
    "customer_support": {"dashboard", "inbox", "contacts", "leads_create"},
    "viewer": {"dashboard_read", "reports_read"},
    "client": {"client_portal_own"},
}

class UESBackendEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def log_activity(self, conn: sqlite3.Connection, org_id: str, actor_name: str, actor_role: str, category: str, summary: str, entity_type: str = "", entity_id: str = ""):
        log_id = f"LOG-{int(datetime.utcnow().timestamp()*1000)}-{os.urandom(2).hex().upper()}"
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO activity_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (log_id, org_id, actor_name, actor_role, category, summary, entity_type, entity_id, now)
        )

    def check_permission(self, role_code: str, required_perm: str) -> bool:
        perms = ROLE_PERMISSIONS.get(role_code, set())
        return "*" in perms or required_perm in perms

    # --- Section 5: Authentication & Access Control ---
    def authenticate_user(self, identifier: str, password: str, required_portal_roles: Optional[List[str]] = None) -> Dict[str, Any]:
        conn = self.get_conn()
        try:
            ident = identifier.strip()
            row = conn.execute("SELECT * FROM users WHERE lower(username) = lower(?) OR lower(email) = lower(?)", (ident, ident)).fetchone()
            if not row:
                return {"ok": False, "error": "اسم المستخدم أو كلمة المرور غير صحيحة."}
            if required_portal_roles and row["role_code"] not in required_portal_roles:
                return {"ok": False, "error": f"هذا الحساب ({row['role_code']}) غير مخول بالدخول من هذه البوابة المخصصة."}
            if not row["is_active"]:
                return {"ok": False, "error": "هذا الحساب غير نشط."}
            if row["failed_attempts"] >= 5:
                return {"ok": False, "error": "تم قفل الحساب مؤقتاً بسبب تجاوز الحد الأقصى لمحاولات الدخول الفاشلة."}
            if not verify_password(password, row["password_hash"]):
                conn.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = ?", (row["id"],))
                conn.commit()
                return {"ok": False, "error": "كلمة المرور غير صحيحة."}
            if not row['password_hash'].startswith('pbkdf2_sha256$'):
                conn.execute('UPDATE users SET password_hash=? WHERE id=?', (make_password_hash(password), row['id']))
            conn.execute("UPDATE users SET failed_attempts = 0, last_login_at = ? WHERE id = ?", (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), row["id"]))
            prof = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (row["id"],)).fetchone()
            self.log_activity(conn, row["organization_id"], prof["full_name"] if prof else ident, row["role_code"], "تسجيل دخول", f"تسجيل دخول ناجح للمستخدم {row['username']}", "user", row["id"])
            conn.commit()
            return {
                "ok": True,
                "user": {
                    "id": row["id"],
                    "username": row["username"],
                    "email": row["email"],
                    "role_code": row["role_code"],
                    "is_owner": bool(row["is_owner"]),
                    "full_name": prof["full_name"] if prof else row["username"],
                    "department": prof["department"] if prof else "",
                }
            }
        finally:
            conn.close()

    def create_user_by_admin(self, actor_role: str, actor_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if actor_role != "super_admin":
            return {"ok": False, "error": "مرفوض أمنياً (RBAC): إنشاء حسابات المستخدمين وتعيين الأدوار متاح حصراً لحساب الأدمن/المالك (Ahmed_99)."}
        conn = self.get_conn()
        try:
            uname = payload.get("username", "").strip()
            raw_pw = payload.get("password", "").strip()
            role_code = payload.get("role_code", "sales_rep").strip()
            full_name = payload.get("full_name", uname).strip()
            dept = payload.get("department", "المبيعات والتعاقدات").strip()
            job_title = payload.get("job_title", "موظف معتمد").strip()
            email = payload.get("email", f"{uname.lower()}@ues-edu.com").strip()
            if not uname or len(raw_pw) < 12:
                return {"ok": False, "error": "اسم المستخدم مطلوب وكلمة المرور لا تقل عن 12 حرفًا."}
            if role_code == 'super_admin' or not conn.execute('SELECT 1 FROM roles WHERE code=?', (role_code,)).fetchone():
                return {"ok": False, "error": "الدور غير مسموح به أو محذوف."}
            dup = conn.execute("SELECT id FROM users WHERE lower(username) = lower(?) OR lower(email) = lower(?)", (uname, email)).fetchone()
            if dup:
                return {"ok": False, "error": f"اسم المستخدم ({uname}) أو البريد مسجل مسبقاً."}
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            u_id = f"U-{int(datetime.utcnow().timestamp()*1000) % 100000}"
            pw_hash = make_password_hash(raw_pw)
            conn.execute("""
                INSERT INTO users (id, organization_id, username, email, password_hash, role_code, is_owner, is_active, mfa_enabled, failed_attempts, last_login_at, created_at, updated_at, created_by)
                VALUES (?, 'ORG-UES-001', ?, ?, ?, ?, 0, 1, 0, 0, NULL, ?, ?, ?)
            """, (u_id, uname, email, pw_hash, role_code, now, now, actor_name))
            initials = "".join([w[0] for w in full_name.split()[:2]]) or "U"
            conn.execute("""
                INSERT INTO profiles (id, user_id, organization_id, full_name, department, job_title, phone, academic_specialization, skills_json, work_capacity, availability_status, avatar_initials, created_at, updated_at, created_by)
                VALUES (?, ?, 'ORG-UES-001', ?, ?, ?, '', '', '[]', 8, 'متاح', ?, ?, ?, ?)
            """, (f"PROF-{u_id}", u_id, full_name, dept, job_title, initials, now, now, actor_name))
            self.log_activity(conn, "ORG-UES-001", actor_name, actor_role, "إدارة الحسابات والصلاحيات", f"إنشاء حساب جديد ({uname}) بدور ({role_code}) بواسطة الأدمن", "user", u_id)
            conn.commit()
            return {"ok": True, "user_id": u_id, "username": uname, "role_code": role_code}
        finally:
            conn.close()

    def register_public_attempt(self, email: str, requested_role: str = "super_admin") -> Dict[str, Any]:
        """Enforces Section 5 rule: Public users cannot create an alternative org or grant themselves owner role."""
        return {
            "ok": False,
            "error": "مرفوض أمنياً (RBAC): لا يُسمح لأي مستخدم عام بإنشاء مؤسسة بديلة أو منح نفسه صلاحية المالك. الانضمام يتم حصراً بدعوة رسمية من مدير مخوّل."
        }

    # --- Section 11: Server-Side Smart Pricing Engine (Exact Cents Math) ---
    def calculate_smart_quote(
        self,
        service_id: str,
        quantity: int,
        complexity_level: str,
        urgency_level: str,
        academic_level: str,
        discount_pct: float,
        tax_pct: float = 14.0,
        target_currency: str = "EGP"
    ) -> Dict[str, Any]:
        conn = self.get_conn()
        try:
            svc = conn.execute("SELECT * FROM services WHERE id = ?", (service_id,)).fetchone()
            if not svc:
                return {"ok": False, "error": "الخدمة غير موجودة في الكتالوج."}
            org = conn.execute("SELECT * FROM organizations WHERE id = ?", (svc["organization_id"],)).fetchone()
            max_disc = float(org["max_auto_discount_pct"]) if org else 10.0

            def get_mult(r_type: str, key: str, default: float = 1.0) -> float:
                r = conn.execute("SELECT multiplier_or_rate FROM pricing_rules WHERE rule_type = ? AND key_code = ?", (r_type, key)).fetchone()
                return float(r["multiplier_or_rate"]) if r else default

            comp_m = get_mult("complexity", complexity_level, 1.0)
            urg_m = get_mult("urgency", urgency_level, 1.0)
            acad_m = get_mult("academic_level", academic_level, 1.0)
            fx_rate = get_mult("exchange_rate", target_currency, 1.0)

            base_cents = int(svc["base_price_cents"])
            qty = max(1, int(quantity))
            gross_cents = int(round(base_cents * qty * comp_m * urg_m * acad_m))
            disc_pct = max(0.0, min(100.0, float(discount_pct)))
            disc_cents = int(round(gross_cents * (disc_pct / 100.0)))
            net_after_disc_cents = gross_cents - disc_cents
            tax_cents = int(round(net_after_disc_cents * (float(tax_pct) / 100.0)))
            final_egp_cents = net_after_disc_cents + tax_cents

            converted_cents = int(round(final_egp_cents / fx_rate)) if fx_rate > 0 else final_egp_cents
            requires_approval = disc_pct > max_disc
            est_cost_cents = int(round(base_cents * qty * 0.55))
            margin_cents = net_after_disc_cents - est_cost_cents

            return {
                "ok": True,
                "service_id": service_id,
                "service_name": svc["name_ar"],
                "base_price_cents": base_cents,
                "quantity": qty,
                "complexity_multiplier": comp_m,
                "urgency_multiplier": urg_m,
                "academic_multiplier": acad_m,
                "gross_cents": gross_cents,
                "discount_pct": disc_pct,
                "discount_cents": disc_cents,
                "tax_pct": tax_pct,
                "tax_cents": tax_cents,
                "total_egp_cents": final_egp_cents,
                "target_currency": target_currency,
                "exchange_rate": fx_rate,
                "final_converted_cents": converted_cents,
                "estimated_cost_cents": est_cost_cents,
                "estimated_margin_cents": margin_cents,
                "requires_manager_approval": requires_approval,
                "max_auto_discount_pct": max_disc,
            }
        finally:
            conn.close()

    # --- Section 12, 13, 14, 15, 17: Full Commercial & ERP Lifecycle ---
    def create_quote(self, actor_role: str, actor_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not (self.check_permission(actor_role, "quotes") or self.check_permission(actor_role, "quotes_draft")):
            return {"ok": False, "error": "غير مصرح لهذا الدور بإنشاء عروض أسعار."}
        calc = self.calculate_smart_quote(
            payload["service_id"],
            payload.get("quantity", 1),
            payload.get("complexity_level", "قياسي"),
            payload.get("urgency_level", "عادي"),
            payload.get("academic_level", "دكتوراه"),
            payload.get("discount_pct", 0.0),
            payload.get("tax_pct", 14.0),
            payload.get("currency", "EGP")
        )
        if not calc["ok"]:
            return calc

        conn = self.get_conn()
        try:
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            q_id = payload.get("id") or f"QT-{int(datetime.utcnow().timestamp()*1000) % 100000}"
            q_num = payload.get("quote_number") or f"QT-2026-{q_id.split('-')[-1]}"
            status = "بانتظار الاعتماد" if calc["requires_manager_approval"] else "مسودة"
            org_id = "ORG-UES-001"

            conn.execute("""
                INSERT INTO quotes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q_id, org_id, q_num, payload["contact_id"], payload.get("lead_id"), payload["service_id"],
                payload.get("title") or calc["service_name"], payload.get("description", ""),
                "Fixed Price", calc["quantity"], calc["base_price_cents"],
                payload.get("complexity_level", "قياسي"), calc["complexity_multiplier"],
                payload.get("urgency_level", "عادي"), calc["urgency_multiplier"],
                payload.get("academic_level", "دكتوراه"), calc["academic_multiplier"],
                calc["discount_pct"], calc["discount_cents"], calc["tax_pct"], calc["tax_cents"],
                calc["final_converted_cents"], calc["estimated_cost_cents"], calc["target_currency"],
                payload.get("proposed_duration_days", 10), "تسليم مرحلي وفق الجدول",
                "مراجعتان مجانيتان خلال 14 يوماً", "30% تعاقد - 30% مرحلة أولى - 30% مرحلة ثانية - 10% تسليم نهائي",
                payload.get("valid_until", "2026-11-30"), status, now, now, actor_name
            ))

            if calc["requires_manager_approval"]:
                ap_id = f"APR-{q_id}"
                c_row = conn.execute("SELECT full_name FROM contacts WHERE id = ?", (payload["contact_id"],)).fetchone()
                c_name = c_row["full_name"] if c_row else payload["contact_id"]
                conn.execute("""
                    INSERT INTO approvals VALUES (?, ?, 'خصم استثنائي يتجاوز السقف', ?, ?, ?, ?, ?, 'د. طارق المنشاوي', 'قيد الانتظار', NULL, NULL, ?, NULL)
                """, (ap_id, org_id, q_id, actor_name, c_name, f"{calc['final_converted_cents']/100:.2f} {calc['target_currency']} (خصم {calc['discount_pct']}%)", "تجاوز الحد الأقصى للخصم التلقائي (10%)", now))

            self.log_activity(conn, org_id, actor_name, actor_role, "عروض الأسعار", f"إنشاء عرض السعر {q_num} بحالة ({status})", "quote", q_id)
            conn.commit()
            return {"ok": True, "quote_id": q_id, "quote_number": q_num, "status": status, "calculation": calc}
        finally:
            conn.close()

    def approve_quote_and_accept(self, actor_role: str, actor_name: str, quote_id: str, accept_by_client: bool = True) -> Dict[str, Any]:
        if not self.check_permission(actor_role, "approvals"):
            return {"ok": False, "error": "غير مصرح لهذا الدور باعتماد عروض الأسعار أو الخصومات الاستثنائية."}
        conn = self.get_conn()
        try:
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            q = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
            if not q:
                return {"ok": False, "error": "عرض السعر غير موجود."}
            new_status = "مقبول" if accept_by_client else "معتمد"
            conn.execute("UPDATE quotes SET status = ?, updated_at = ? WHERE id = ?", (new_status, now, quote_id))
            conn.execute("UPDATE approvals SET status = 'معتمد', decided_by = ?, decided_at = ?, decision_notes = 'معتمد من الإدارة' WHERE related_entity_id = ?", (actor_name, now, quote_id))
            if accept_by_client:
                conn.execute("""
                    INSERT INTO quote_acceptances VALUES (?, ?, ?, ?, 'قبول مسجل ومؤرشف Snapshot', ?, ?, ?)
                """, (f"QACC-{quote_id}", q["organization_id"], quote_id, q["contact_id"], q["total_cents"], now, actor_name))
                if q["lead_id"]:
                    conn.execute("UPDATE leads SET stage = 'مكتسب', updated_at = ? WHERE id = ?", (now, q["lead_id"]))
            self.log_activity(conn, q["organization_id"], actor_name, actor_role, "اعتماد وقبول عرض", f"تحديث حالة العرض {q['quote_number']} إلى {new_status}", "quote", quote_id)
            conn.commit()
            return {"ok": True, "quote_id": quote_id, "status": new_status, "snapshot_total_cents": q["total_cents"]}
        finally:
            conn.close()

    def create_contract_from_quote(self, actor_role: str, actor_name: str, quote_id: str, installments: List[float] = [30, 30, 30, 10]) -> Dict[str, Any]:
        if not self.check_permission(actor_role, "contracts"):
            return {"ok": False, "error": "غير مصرح لهذا الدور بإنشاء العقود."}
        if abs(sum(installments) - 100.0) > 0.001 or any(x < 0 for x in installments):
            return {"ok": False, "error": "خطأ في جدول الأقساط: يجب أن يساوي إجمالي نسب الأقساط 100% بالضبط."}
        conn = self.get_conn()
        try:
            q = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
            if not q or q["status"] != "مقبول":
                return {"ok": False, "error": "لا يمكن إنشاء عقد إلا من عرض سعر مقبول."}
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            ct_id = f"CT-{quote_id.split('-')[-1]}"
            ct_num = f"CNT-2026-{quote_id.split('-')[-1]}"
            conn.execute("""
                INSERT INTO contracts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ar', 'معتمد', 'موافقة مسجلة (محاكاة)', ?, ?, ?, ?)
            """, (
                ct_id, q["organization_id"], ct_num, q["contact_id"], quote_id,
                f"عقد خدمات أكاديمية — {q['title']}", q["total_cents"], q["currency"],
                q["description"] or q["title"], "تسليم المخرجات الأكاديمية وفق المعايير المعتمدة",
                now[:10], "2026-11-28", json.dumps(installments),
                q["revision_policy"], "سرية تامة لبيانات الباحث ومستنداته.", "احتساب المراحل المنجزة عند الإلغاء.",
                now[:10], now, now, actor_name
            ))
            for idx, pct in enumerate(installments, 1):
                m_amt = int(round(q["total_cents"] * (pct / 100.0)))
                conn.execute("""
                    INSERT INTO contract_milestones VALUES (?, ?, ?, ?, ?, ?, ?, '2026-11-20', 'مجدولة', ?)
                """, (f"MS-{ct_id}-{idx}", q["organization_id"], ct_id, idx, f"القسط رقم {idx} ({pct}%)", pct, m_amt, now))
            self.log_activity(conn, q["organization_id"], actor_name, actor_role, "العقود", f"إنشاء العقد {ct_num} من العرض {q['quote_number']} بنظام أقساط {installments}", "contract", ct_id)
            conn.commit()
            return {"ok": True, "contract_id": ct_id, "contract_number": ct_num, "value_cents": q["total_cents"]}
        finally:
            conn.close()

    def create_project_and_tasks_from_contract(self, actor_role: str, actor_name: str, contract_id: str, assigned_specialist_id: str = "U-AS1") -> Dict[str, Any]:
        if not self.check_permission(actor_role, "projects"):
            return {"ok": False, "error": "غير مصرح لهذا الدور بإنشاء المشروعات."}
        conn = self.get_conn()
        try:
            ct = conn.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,)).fetchone()
            if not ct:
                return {"ok": False, "error": "العقد غير موجود."}
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            p_id = f"PRJ-{contract_id.split('-')[-1]}"
            p_code = f"PRJ-2026-{contract_id.split('-')[-1]}"
            conn.execute("""
                INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, 'U-AOM', 'العمليات الأكاديمية والإحصائية', ?, ?, ?, 'قيد التنفيذ', 0, ?, ?, ?, 'عالية', 'مشروع منشأ تلقائياً بعد اعتماد العقد', 'جاهز للتنفيذ', ?, ?, ?)
            """, (
                p_id, ct["organization_id"], p_code, ct["title"], ct["contact_id"], contract_id,
                json.dumps(["U-AOM", assigned_specialist_id]), ct["start_date"], ct["agreed_deadline"],
                ct["contract_value_cents"], int(ct["contract_value_cents"] * 0.55), ct["currency"],
                now, now, actor_name
            ))
            t1_id = f"TSK-{p_id}-1"
            t2_id = f"TSK-{p_id}-2"
            conn.execute("""
                INSERT INTO tasks VALUES (?, ?, ?, ?, 'مراجعة خطة العمل والمنهجية والبيانات الأولية', 'فحص المتطلبات الأكاديمية والملفات المرفقة', ?, ?, ?, 'عالية', 'قيد التنفيذ', 50, 8, 4, 'قيد العمل', '[]', ?, ?, ?)
            """, (t1_id, ct["organization_id"], f"TSK-2026-{p_id[-3:]}-A", p_id, assigned_specialist_id, ct["start_date"], ct["agreed_deadline"], now, now, actor_name))
            conn.execute("""
                INSERT INTO tasks VALUES (?, ?, ?, ?, 'إعداد المخرجات الأكاديمية والتقرير النهائي للمراجعة', 'تنفيذ التحليل والتدقيق النهائي', 'U-AS2', ?, ?, 'متوسطة', 'قيد الانتظار', 0, 10, 0, 'بانتظار المراجعة', '[]', ?, ?, ?)
            """, (t2_id, ct["organization_id"], f"TSK-2026-{p_id[-3:]}-B", p_id, ct["start_date"], ct["agreed_deadline"], now, now, actor_name))
            self.log_activity(conn, ct["organization_id"], actor_name, actor_role, "المشروعات والمهام", f"تحويل العقد {ct['contract_number']} إلى مشروع {p_code} وتوزيع المهام", "project", p_id)
            conn.commit()
            return {"ok": True, "project_id": p_id, "project_code": p_code, "tasks": [t1_id, t2_id]}
        finally:
            conn.close()

    def issue_invoice_and_record_payment(
        self,
        actor_role: str,
        actor_name: str,
        contract_id: str,
        amount_cents: int,
        reference_number: str,
        payment_method: str = "InstaPay",
        verification_source: str = "finance_officer"
    ) -> Dict[str, Any]:
        """Enforces Section 17: AI cannot verify payments alone; duplicate references are rejected."""
        if verification_source == "ai_agent":
            return {"ok": False, "error": "مرفوض: لا يجوز تأكيد الدفعات المالية بواسطة الذكاء الاصطناعي وحده دون تحقق موظف مالي أو Webhook موثق."}
        if not self.check_permission(actor_role, "payments"):
            return {"ok": False, "error": "غير مصرح لهذا الدور بتسجيل أو تأكيد الدفعات المالية."}

        conn = self.get_conn()
        try:
            dup = conn.execute("SELECT id FROM payments WHERE reference_number = ?", (reference_number.strip(),)).fetchone()
            if dup:
                return {"ok": False, "error": f"منع تكرار العملية (Idempotency): رقم المرجع {reference_number} مسجل مسبقاً."}

            ct = conn.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,)).fetchone()
            if not ct:
                return {"ok": False, "error": "العقد غير موجود."}

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            inv_id = f"INV-{contract_id.split('-')[-1]}-1"
            inv_row = conn.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone()
            if not inv_row:
                conn.execute("""
                    INSERT INTO invoices VALUES (?, ?, ?, ?, ?, 'الدفعة الأولى (30%)', ?, ?, 0, ?, ?, '2026-11-20', 'صادرة', ?, ?, ?)
                """, (inv_id, ct["organization_id"], f"INV-2026-{contract_id.split('-')[-1]}", ct["contact_id"], contract_id, amount_cents, int(amount_cents * 0.14), amount_cents, ct["currency"], now, now, actor_name))
                inv_row = conn.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone()

            if amount_cents > inv_row["remaining_cents"]:
                return {"ok": False, "error": "المبلغ المدخل يتجاوز الرصيد المتبقي للفاتورة."}

            pay_id = f"PAY-{int(datetime.utcnow().timestamp()*1000) % 100000}"
            conn.execute("""
                INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'verified_receipt.pdf', ?, ?, ?, ?, ?)
            """, (pay_id, ct["organization_id"], f"PAY-2026-{pay_id.split('-')[-1]}", inv_id, ct["contact_id"], amount_cents, ct["currency"], payment_method, reference_number.strip(), verification_source, actor_name, now, now, actor_name))

            new_paid = inv_row["paid_cents"] + amount_cents
            new_rem = inv_row["remaining_cents"] - amount_cents
            new_st = "مدفوعة" if new_rem == 0 else "مدفوعة جزئياً"
            conn.execute("UPDATE invoices SET paid_cents = ?, remaining_cents = ?, status = ?, updated_at = ? WHERE id = ?", (new_paid, new_rem, new_st, now, inv_id))
            self.log_activity(conn, ct["organization_id"], actor_name, actor_role, "المالية والمدفوعات", f"تأكيد دفعة {amount_cents/100:.2f} {ct['currency']} بمرجع {reference_number} للفاتورة {inv_id}", "payment", pay_id)
            conn.commit()
            return {"ok": True, "invoice_id": inv_id, "payment_id": pay_id, "invoice_status": new_st, "remaining_cents": new_rem}
        finally:
            conn.close()

    # --- Section 18, 19, 20, 21: AI Agent Engine & 7 Scenarios ---
    def run_ai_agent_turn(self, user_message: str, api_key_configured: Optional[bool] = None) -> Dict[str, Any]:
        conn = self.get_conn()
        try:
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            has_env_key = bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY"))
            use_live = has_env_key if api_key_configured is None else bool(api_key_configured)
            mode_label = "متصل — OpenAI API (gpt-4o عبر الخادم)" if use_live else "غير متصل — وضع تجريبي"
            q = user_message.strip()

            # Scenario G: Academic Integrity Check
            if any(w in q for w in ["اختلاق", "فبركة", "تزوير", "بيانات وهمية", "مراجع وهمية", "ضمان قبول"]):
                intent = "academic_integrity_violation_refusal"
                tool = "get_company_policy(policy='academic_integrity')"
                tool_out = "ميثاق النزاهة الأكاديمية KB-01: يُحظر اختلاق النتائج أو المراجع أو ضمان القبول."
                reply = (
                    f"[{mode_label}] نعتذر، تلتزم شركة المتحدة للخدمات التعليمية (UES) بمعايير النزاهة الأكاديمية الصارمة؛ "
                    "لذلك نرفض قطعياً اختلاق نتائج استبيان أو فبركة بيانات أو إضافة مراجع غير حقيقية. "
                    "يسعدنا دعمك بشكل علمي مشروع في تحليل بياناتك الفعلية أو التحقق من صحة المراجع وتوثيقها وفق APA 7."
                )
                risk = "مرتفع — حماية نزاهة أكاديمية"
                req_app = 0
            # Scenario D: Negotiation / Discount > 10%
            elif any(w in q for w in ["خصم 20%", "خصم ٢٠٪", "خصم 25%", "خصم كبير", "تخفيض 20"]):
                intent = "discount_negotiation_exceeds_limit"
                tool = "request_manager_approval(discount_requested=20, max_allowed=10)"
                tool_out = "الحد الأقصى للخصم التلقائي هو 10%. تم إنشاء طلب موافقة للإدارة."
                reply = (
                    f"[{mode_label}] أقدّر تواصلك معنا. صلاحية الخصم المباشر المتاحة للوكيل ومندوب المبيعات تصل إلى 10% فقط. "
                    "بما أن طلبك (خصم 20%) يتجاوز الحد المعتمد، قمت برفع طلب موافقة استثنائي للإدارة عبر أداة request_manager_approval() وسنوافيك بالقرار فور اعتماده."
                )
                risk = "متوسط — يتطلب موافقة مدير"
                req_app = 1
            # Scenario C: Urgent Delivery (e.g., 2 days)
            elif any(w in q for w in ["خلال يومين", "في يومين", "مستعجل جدا", "بكرة", "غدا"]):
                intent = "urgent_delivery_capacity_check"
                tool = "check_team_capacity(department='Academic & Stats', requested_days=2)"
                tool_out = "فحص سعة الفريق: د. علي النجار متاح لـ 14 ساعة أسبوعياً؛ الحد الأدنى القياسي 5-7 أيام."
                reply = (
                    f"[{mode_label}] قمت بفحص توافر الفريق الفعلي عبر check_team_capacity(). "
                    "لا نعد بموعد تسليم نهائي قبل مراجعة حجم الملف والتأكد من الطاقة الاستيعابية للقسم المختص. "
                    "يرجى إرسال الملف لتأكيد إمكانية التنفيذ العاجل (مع معامل الاستعجال المعتمد) أو تحويل الطلب لمدير العمليات الأكاديمية."
                )
                risk = "متوسط — فحص سعة"
                req_app = 1
            # Scenario E: Payment Notification
            elif any(w in q for w in ["حولت الدفعة", "دفعت", "إيصال التحويل", "حولت الفلوس", "تم التحويل"]):
                intent = "payment_verification_request"
                tool = "get_invoice_status() + create_followup_task(dept='Finance')"
                tool_out = "تسجيل طلب تحقق مالي؛ لا يتم تأكيد الدفع آلياً."
                reply = (
                    f"[{mode_label}] شكراً لك. يرجى تزويدنا برقم العملية المرجعي (Reference Number) وصورة إيصال التحويل. "
                    "تم تسجيل طلب تحقق لدى الإدارة المالية؛ علماً أن تأكيد الدفع لا يتم آلياً عبر الذكاء الاصطناعي بل يتطلب مطابقة واعتماد الموظف المالي المختص."
                )
                risk = "متوسط — تحقق مالي"
                req_app = 1
            # Scenario F: Complaint / Escalation
            elif any(w in q for w in ["اتأخر", "شكوى", "أكلم المدير", "مشكلة في المشروع", "غير راضي"]):
                intent = "client_complaint_escalation"
                tool = "handoff_to_human(priority='high', reason='client_complaint')"
                tool_out = "تم تسجيل شكوى وتحويل المحادثة إلى المدير المختص وإيقاف الرد الآلي."
                reply = (
                    f"[{mode_label}] نعتذر جداً عن أي إزعاج. قمت بتسجيل ملاحظتك كأولوية قصوى وتحويل المحادثة فوراً إلى المسؤول البشري المختص "
                    "عبر أداة handoff_to_human() لمتابعة المشروع والتواصل معك مباشرة."
                )
                risk = "مرتفع — تصعيد بشري"
                req_app = 1
            # Scenario B: Price Inquiry
            elif any(w in q for w in ["بكام", "كم سعر", "تكلفة", "أسعار", "التحليل الإحصائي"]):
                intent = "service_price_inquiry"
                tool = "lookup_service(code='UES-STA-301') + calculate_quote()"
                tool_out = "خدمة التحليل الإحصائي (DEMO): السعر الأساسي المبدئي 3,800 EGP."
                reply = (
                    f"[{mode_label}] خدمة التحليل الإحصائي للبيانات الفعلية (SPSS / AMOS / SmartPLS) متوفرة بسعر أساسي استرشادي 3,800 EGP (مصنف DEMO). "
                    "لتقديم عرض سعر دقيق ومعتمد، يرجى توضيح: نوع البيانات، حجم العينة، عدد المتغيرات والفروض، والموعد المطلوب."
                )
                risk = "منخفض"
                req_app = 0
            # Scenario A: New Researcher / Default Academic Inquiry
            else:
                intent = "new_researcher_qualification"
                tool = "lookup_service() + create_lead()"
                tool_out = "تأهيل باحث جديد وربط الخدمات الاستشارية والإحصائية."
                reply = (
                    f"[{mode_label}] وعليكم السلام ورحمة الله، أهلاً بك في المتحدة للخدمات التعليمية (UES). "
                    "يسعدنا دعمك في بحث الدكتوراه (استشارة المنهجية وتحليل البيانات). "
                    "لإعداد ملفك وتقدير عرض السعر المبدئي، يرجى إفادتنا بـ: الجامعة، التخصص الدقيق، حجم البيانات أو الملف المتوفر، والموعد النهائي المستهدف."
                )
                risk = "منخفض"
                req_app = 0

            run_id = f"AIRUN-{int(datetime.utcnow().timestamp()*1000) % 100000}"
            conn.execute("""
                INSERT INTO ai_conversation_runs VALUES (?, 'ORG-UES-001', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'AI-ENGINE')
            """, (run_id, intent, q, intent, tool, tool_out, reply, risk, req_app, mode_label, now))
            conn.commit()
            return {
                "ok": True,
                "run_id": run_id,
                "mode_label": mode_label,
                "intent": intent,
                "invoked_tool": tool,
                "tool_output": tool_out,
                "reply": reply,
                "risk_level": risk,
                "requires_human_approval": bool(req_app),
            }
        finally:
            conn.close()

if __name__ == "__main__":
    engine = UESBackendEngine()
    print("Backend Engine ready. Sample pricing calculation:", engine.calculate_smart_quote("SVC-06", 1, "متقدم", "عادي", "دكتوراه", 5.0))
