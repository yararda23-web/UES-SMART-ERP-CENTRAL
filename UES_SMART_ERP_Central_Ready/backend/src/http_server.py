#!/usr/bin/env python3
"""Local UES Desktop HTTP server with authenticated sessions and owner-only role APIs.

Local demo security hardening; this is NOT a certified production IAM system.
"""
import json
import os
import secrets
import sqlite3
import threading
import time
from pathlib import Path
from http import cookies
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from server import UESBackendEngine, make_password_hash, verify_password

PORT = int(os.environ.get('PORT', '8765'))
HOST = '127.0.0.1'
BASE = Path(__file__).resolve().parents[2]
FRONTEND = Path(os.environ.get('UES_FRONTEND_PATH', str(BASE / 'frontend' / 'dist'))).resolve()
DB_PATH = Path(os.environ.get('UES_DB_PATH', str(BASE / 'database' / 'ues_smart_erp.db'))).resolve()
ALLOWED_TABLES = {'organizations','roles','permissions','users','profiles','memberships','invitations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','quote_approvals','quote_acceptances','contracts','contract_milestones','projects','project_members','tasks','task_comments','team_availability','invoices','payments','expenses','agents','knowledge_documents','ai_conversation_runs','automation_rules','automation_runs','notifications','approvals','files','settings','activity_logs','webhook_events','integration_connections','client_portal_access'}
IDENTITY_TABLES = {'users','roles','permissions','memberships','invitations','profiles','activity_logs'}
PUBLIC_NAMES = {'id','username','email','role_code','is_owner','is_active','organization_id','last_login_at','created_at','updated_at'}
ROLE_READ = {
    'general_manager': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','quote_approvals','quote_acceptances','contracts','contract_milestones','projects','project_members','tasks','task_comments','team_availability','agents','knowledge_documents','ai_conversation_runs','automation_rules','notifications','approvals','files','activity_logs'},
    'sales_manager': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','quote_approvals','quote_acceptances','contracts','contract_milestones','notifications','approvals'},
    'sales_rep': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','service_categories','services','pricing_rules','quotes','quote_items','notifications'},
    'academic_manager': {'organizations','contacts','service_categories','services','projects','project_members','tasks','task_comments','team_availability','knowledge_documents','files','notifications'},
    'academic_specialist': {'organizations','contacts','projects','project_members','tasks','task_comments','files','notifications'},
    'finance_manager': {'organizations','contacts','contracts','contract_milestones','invoices','payments','expenses','notifications','approvals'},
    'customer_support': {'organizations','contacts','contact_identities','channels','conversations','messages','message_attachments','leads','lead_activities','notifications'},
    'viewer': {'organizations'},
    'client': {'organizations','contacts','contracts','contract_milestones','projects','tasks','invoices','payments','files','client_portal_access','notifications'}
}
ROLE_WRITE = {
    'general_manager': {'contacts','leads','lead_activities','conversations','messages','projects','tasks','task_comments','project_members','team_availability','quotes','quote_items','files','notifications'},
    'sales_manager': {'contacts','contact_identities','leads','lead_activities','conversations','messages','quotes','quote_items','quote_approvals','quote_acceptances','notifications'},
    'sales_rep': {'contacts','contact_identities','leads','lead_activities','conversations','messages','quotes','quote_items','notifications'},
    'academic_manager': {'projects','tasks','task_comments','project_members','team_availability','files','notifications'},
    'academic_specialist': {'tasks','task_comments','notifications'},
    'finance_manager': {'invoices','expenses','notifications'},
    'customer_support': {'contacts','contact_identities','leads','lead_activities','conversations','messages','notifications'}
}
# NOTE: payments are blocked from generic snapshots: must use a dedicated verified-finance API.
PROTECTED_WRITE = IDENTITY_TABLES | {'payments','integration_connections','webhook_events'}
SESSION_TTL = 8 * 60 * 60
SESSIONS = {}
SESSION_LOCK = threading.Lock()


def get_db():
    c = sqlite3.connect(str(DB_PATH), timeout=10)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    c.execute('PRAGMA busy_timeout=10000')
    return c


def _raw_state():
    with get_db() as c:
        c.execute('CREATE TABLE IF NOT EXISTS desktop_ui_state (id INTEGER PRIMARY KEY CHECK(id=1), snapshot_json TEXT NOT NULL, saved_at TEXT DEFAULT CURRENT_TIMESTAMP)')
        existing = c.execute('SELECT snapshot_json FROM desktop_ui_state WHERE id=1').fetchone()
        base = json.loads(existing['snapshot_json']) if existing else {}
        for table in ALLOWED_TABLES:
            if table in IDENTITY_TABLES or table not in base:
                try:
                    base[table] = [dict(row) for row in c.execute('SELECT * FROM "' + table + '"')]
                except sqlite3.OperationalError:
                    base[table] = []
        return base


def _save_state(data):
    payload = json.dumps({k: data.get(k,[]) for k in ALLOWED_TABLES},ensure_ascii=False)
    with get_db() as c:
        c.execute('CREATE TABLE IF NOT EXISTS desktop_ui_state (id INTEGER PRIMARY KEY CHECK(id=1), snapshot_json TEXT NOT NULL, saved_at TEXT DEFAULT CURRENT_TIMESTAMP)')
        c.execute('INSERT INTO desktop_ui_state(id,snapshot_json,saved_at) VALUES (1,?,CURRENT_TIMESTAMP) ON CONFLICT(id) DO UPDATE SET snapshot_json=excluded.snapshot_json,saved_at=CURRENT_TIMESTAMP',(payload,))
    return len(payload)


def _user_for_session(handler):
    jar=cookies.SimpleCookie()
    try: jar.load(handler.headers.get('Cookie',''))
    except cookies.CookieError: return None
    token = jar.get('UES_SESSION')
    if not token: return None
    with SESSION_LOCK:
        sess = SESSIONS.get(token.value)
        if not sess or sess['expires'] <= time.time():
            SESSIONS.pop(token.value,None)
            return None
        user_id = sess['user_id']
    with get_db() as c:
        row=c.execute('SELECT * FROM users WHERE id=? AND is_active=1',(user_id,)).fetchone()
        if row is None: return None
        return dict(row)


def _safe_user(user):
    return {k: user[k] for k in PUBLIC_NAMES if k in user}


def _scope_rows(table, rows, role, user, all_state):
    if role == 'academic_specialist':
        my_id=user['id']
        my_proj={t['project_id'] for t in all_state.get('tasks',[]) if t.get('assigned_to') == my_id}
        my_proj.update({p['project_id'] for p in all_state.get('project_members',[]) if p.get('user_id') == my_id})
        if table == 'tasks': return [x for x in rows if x.get('assigned_to') == my_id]
        if table in ('projects','project_members'): return [x for x in rows if x.get('id') in my_proj or x.get('project_id') in my_proj]
        if table == 'files': return [x for x in rows if x.get('project_id') in my_proj and x.get('access_level') != 'داخلي سري']
        if table == 'contacts':
            contacts={p.get('contact_id') for p in all_state.get('projects',[]) if p.get('id') in my_proj}
            return [x for x in rows if x.get('id') in contacts]
    if role == 'client':
        ids={x.get('contact_id') for x in all_state.get('client_portal_access',[]) if x.get('user_id') == user['id']}
        if table == 'client_portal_access': return [x for x in rows if x.get('user_id') == user['id']]
        if table == 'contacts': return [x for x in rows if x.get('id') in ids]
        proj={x.get('id') for x in all_state.get('projects',[]) if x.get('contact_id') in ids}
        contracts={x.get('id') for x in all_state.get('contracts',[]) if x.get('contact_id') in ids}
        invoices={x.get('id') for x in all_state.get('invoices',[]) if x.get('contract_id') in contracts}
        if table == 'projects': return [x for x in rows if x.get('id') in proj]
        if table == 'contracts': return [x for x in rows if x.get('id') in contracts]
        if table == 'contract_milestones': return [x for x in rows if x.get('contract_id') in contracts]
        if table == 'tasks': return [x for x in rows if x.get('project_id') in proj]
        if table == 'invoices': return [x for x in rows if x.get('id') in invoices]
        if table == 'payments': return [x for x in rows if x.get('invoice_id') in invoices]
        if table == 'files': return [x for x in rows if x.get('project_id') in proj and x.get('access_level') != 'داخلي سري']
    return rows


def expose_state(data,user):
    role=user['role_code']
    visible = ALLOWED_TABLES if role == 'super_admin' else ROLE_READ.get(role,set())
    output={}
    for t in ALLOWED_TABLES:
        rows = data.get(t,[]) if t in visible else []
        rows = _scope_rows(t,rows,role,user,data)
        if t == 'users':
            rows = [dict((k,v) for k,v in x.items() if k in PUBLIC_NAMES) for x in rows]
        if t == 'profiles' and role != 'super_admin':
            rows = [x for x in rows if x.get('user_id')==user['id']]
        if t in ('integration_connections','channels'):
            rows=[dict((k,v) for k,v in x.items() if not any(y in k.lower() for y in ('secret','token','api_key','password','credential','config'))) for x in rows]
        output[t]=rows
    if role!='super_admin':
        output['users']=[_safe_user(user)]
        output['roles']=[]
        output['permissions']=[]
        output['memberships']=[]
        output['profiles']=[x for x in data.get('profiles',[]) if x.get('user_id')==user['id']]
    return output


def merge_authorized_state(incoming, user):
    if not isinstance(incoming,dict): raise ValueError('Invalid state')
    raw=_raw_state()
    allowed_read=expose_state(raw,user)
    role=user['role_code']
    writable = (ALLOWED_TABLES - PROTECTED_WRITE) if role=='super_admin' else ROLE_WRITE.get(role,set())
    for table, proposed in incoming.items():
        if table not in ALLOWED_TABLES: continue
        if not isinstance(proposed,list): raise ValueError('Invalid table data')
        before=allowed_read.get(table,[])
        if table in PROTECTED_WRITE:
            # Ignore browser copies of protected tables; DB is authoritative.
            continue
        if proposed == before: continue
        if table not in writable:
            raise PermissionError('لا تملك صلاحية تعديل قسم ' + table)
        if role=='academic_specialist':
            # Specialists may only change limited fields of *their own* assigned tasks.
            if table != 'tasks': raise PermissionError('التعديل غير مصرح به')
            old_by_id={x['id']:x for x in before}
            new_by_id={x['id']:x for x in proposed}
            if old_by_id.keys()!=new_by_id.keys(): raise PermissionError('لا يمكن تغيير إسناد المهام')
            for k,old in old_by_id.items():
                delta={a for a in set(old)|set(new_by_id[k]) if old.get(a)!=new_by_id[k].get(a)}
                if delta-{'status','progress_percentage','updated_at'}: raise PermissionError('تعديل حقول غير مسموح بها')
        # Merge rows visible to this user only; never erase invisible records.
        visible_ids={x.get('id') for x in before}
        kept=[x for x in raw.get(table,[]) if x.get('id') not in visible_ids]
        raw[table]=kept+proposed
    return raw


def delete_role(user, code, replacement):
    if user['role_code']!='super_admin' or not user['is_owner']:
        raise PermissionError('صلاحية حذف الأدوار للمالك فقط')
    if code=='super_admin': raise ValueError('لا يمكن حذف دور مالك النظام')
    with get_db() as c:
        role=c.execute('SELECT * FROM roles WHERE code=?',(code,)).fetchone()
        if role is None: raise ValueError('الدور غير موجود')
        users=c.execute('SELECT id FROM users WHERE role_code=?',(code,)).fetchall()
        if users:
            target=c.execute('SELECT * FROM roles WHERE code=?',(replacement,)).fetchone()
            if target is None or replacement in ('super_admin',code):
                raise ValueError('يجب تحديد دور بديل صالح غير دور المالك')
            if c.execute('SELECT 1 FROM users WHERE role_code=? AND is_owner=1',(code,)).fetchone():
                raise ValueError('لا يمكن نقل حساب مالك النظام')
            c.execute('UPDATE users SET role_code=?,updated_at=CURRENT_TIMESTAMP WHERE role_code=?',(replacement,code))
            c.execute('UPDATE memberships SET role_id=? WHERE role_id=?',(target['id'],role['id']))
            c.execute('UPDATE invitations SET role_code=? WHERE role_code=?',(replacement,code))
        c.execute('DELETE FROM permissions WHERE role_id=?',(role['id'],))
        c.execute('DELETE FROM roles WHERE id=?',(role['id'],))
        c.execute('INSERT INTO activity_logs(id,organization_id,actor_name,actor_role,category,action_summary,entity_type,entity_id,created_at) VALUES (?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)',(f'LOG-ROLE-{secrets.token_hex(8)}',user['organization_id'],user['username'],'super_admin','الصلاحيات',f'حذف دور {code}; إعادة إسناد {len(users)} مستخدمين إلى {replacement or "لا يوجد"}','role',code))
    # Refresh the authority tables in saved snapshot automatically via _raw_state().
    return {'ok':True,'deleted_role':code,'reassigned_users':len(users)}


class Handler(BaseHTTPRequestHandler):
    def reply(self,value,status=200,headers=None):
        b=json.dumps(value,ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        if headers:
            for key,val in headers.items(): self.send_header(key,val)
        self.send_header('Content-Length',str(len(b)))
        self.end_headers();self.wfile.write(b)

    def serve_file(self,filepath,content_type):
        if not filepath.is_file(): return self.reply({'ok':False,'error':'Static asset missing'},404)
        b=filepath.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type',content_type)
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(b)))
        self.end_headers();self.wfile.write(b)

    def same_origin(self):
        origin=self.headers.get('Origin','')
        host=self.headers.get('Host','')
        return host in (f'{HOST}:{PORT}',f'localhost:{PORT}') and (not origin or origin in (f'http://{HOST}:{PORT}',f'http://localhost:{PORT}'))

    def require_user(self):
        user=_user_for_session(self)
        if not user: self.reply({'ok':False,'error':'الجلسة غير مصرح بها؛ سجل الدخول مجددًا'},401)
        return user

    def do_GET(self):
        if not self.same_origin(): return self.reply({'ok':False,'error':'Bad origin'},403)
        path=urlparse(self.path).path
        if path in ('/','/index.html','/app'):
            return self.serve_file(FRONTEND/'UES_SMART_ERP.html','text/html; charset=utf-8')
        if path == '/assets/ues.css': return self.serve_file(FRONTEND/'assets'/'ues.css','text/css; charset=utf-8')
        if path == '/api/health': return self.reply({'ok':True,'service':'UES-SMART-ERP-LOCAL','database':'sqlite'})
        if path == '/api/auth/session':
            user = self.require_user()
            if user: return self.reply({'ok':True,'user':_safe_user(user)})
            return
        if path == '/api/state':
            user=self.require_user()
            if user: return self.reply({'ok':True,'database':expose_state(_raw_state(),user)})
            return
        return self.reply({'ok':False,'error':'Not found'},404)

    def do_POST(self):
        if not self.same_origin(): return self.reply({'ok':False,'error':'Bad origin'},403)
        if self.headers.get('Content-Type','').split(';')[0].strip().lower()!='application/json':
            return self.reply({'ok':False,'error':'JSON required'},415)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<1 or length>12_000_000: return self.reply({'ok':False,'error':'Invalid payload size'},413)
            body=json.loads(self.rfile.read(length))
            if not isinstance(body,dict): raise ValueError()
        except (ValueError,UnicodeError): return self.reply({'ok':False,'error':'Malformed JSON'},400)
        path=urlparse(self.path).path
        if path=='/api/auth/login':
            result=UESBackendEngine(str(DB_PATH)).authenticate_user(str(body.get('username','')),str(body.get('password','')))
            if not result.get('ok'): return self.reply({'ok':False,'error':result.get('error','بيانات الدخول غير صحيحة')},401)
            token=secrets.token_urlsafe(48)
            with SESSION_LOCK: SESSIONS[token]={'user_id':result['user']['id'],'expires':time.time()+SESSION_TTL}
            return self.reply({'ok':True,'user':result['user']},headers={'Set-Cookie':f'UES_SESSION={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={SESSION_TTL}'})
        if path=='/api/auth/logout':
            jar=cookies.SimpleCookie()
            try: jar.load(self.headers.get('Cookie',''))
            except cookies.CookieError: pass
            if jar.get('UES_SESSION'):
                with SESSION_LOCK: SESSIONS.pop(jar['UES_SESSION'].value,None)
            return self.reply({'ok':True},headers={'Set-Cookie':'UES_SESSION=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0'})
        user=self.require_user()
        if not user: return
        try:
            if path=='/api/auth/change-password':
                old=str(body.get('old_password',''))
                new=str(body.get('new_password',''))
                if len(new)<12 or old==new: raise ValueError('كلمة المرور الجديدة يجب أن تكون مختلفة ولا تقل عن 12 حرفًا')
                if not verify_password(old,user['password_hash']): raise PermissionError('كلمة المرور الحالية غير صحيحة')
                with get_db() as c:
                    c.execute('UPDATE users SET password_hash=?,failed_attempts=0,updated_at=CURRENT_TIMESTAMP WHERE id=?',(make_password_hash(new),user['id']))
                    c.execute('INSERT INTO activity_logs(id,organization_id,actor_name,actor_role,category,action_summary,entity_type,entity_id,created_at) VALUES (?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)',(f'LOG-MYPASS-{secrets.token_hex(8)}',user['organization_id'],user['username'],user['role_code'],'الأمان','تم تغيير كلمة المرور بواسطة صاحب الحساب','user',user['id']))
                return self.reply({'ok':True,'message':'تم تغيير كلمة المرور بنجاح'})
            if path=='/api/state':
                merged=merge_authorized_state(body.get('database'),user)
                size=_save_state(merged)
                return self.reply({'ok':True,'saved':True,'bytes':size})
            if path=='/api/admin/roles/delete':
                return self.reply(delete_role(user,str(body.get('role_code','')),str(body.get('replacement_role',''))))
            if path=='/api/admin/users/create':
                if user['role_code']!='super_admin' or not user['is_owner']: raise PermissionError('إنشاء المستخدمين للمالك فقط')
                result=UESBackendEngine(str(DB_PATH)).create_user_by_admin('super_admin',user['username'],body)
                return self.reply(result,200 if result.get('ok') else 400)
            if path=='/api/admin/users/reset-password':
                if user['role_code']!='super_admin' or not user['is_owner']: raise PermissionError('إعادة تعيين كلمات المرور للمالك فقط')
                target=str(body.get('user_id',''))
                new_password=secrets.token_urlsafe(18)
                with get_db() as c:
                    target_row=c.execute('SELECT id,username FROM users WHERE id=?',(target,)).fetchone()
                    if not target_row: raise ValueError('المستخدم غير موجود')
                    c.execute('UPDATE users SET password_hash=?,failed_attempts=0,updated_at=CURRENT_TIMESTAMP WHERE id=?',(make_password_hash(new_password),target))
                    c.execute('INSERT INTO activity_logs(id,organization_id,actor_name,actor_role,category,action_summary,entity_type,entity_id,created_at) VALUES (?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)',(f'LOG-PASS-{secrets.token_hex(8)}',user['organization_id'],user['username'],'super_admin','إدارة المستخدمين',f'إعادة تعيين كلمة مرور المستخدم {target_row["username"]}','user',target))
                with SESSION_LOCK:
                    for token,sess in list(SESSIONS.items()):
                        if sess['user_id']==target and sess['user_id']!=user['id']: SESSIONS.pop(token,None)
                return self.reply({'ok':True,'temporary_password':new_password,'notice':'تعرض كلمة المرور المؤقتة مرة واحدة فقط. أرسلها للمستخدم عبر قناة آمنة ثم غيّرها.'})
            if path=='/api/pricing/calculate':
                role=user['role_code']
                if role not in ('super_admin','general_manager','sales_manager','sales_rep'):
                    raise PermissionError('غير مصرح بالتسعير')
                return self.reply(UESBackendEngine(str(DB_PATH)).calculate_smart_quote(body.get('service_id','SVC-06'),body.get('quantity',1),body.get('complexity_level','قياسي'),body.get('urgency_level','عادي'),body.get('academic_level','دكتوراه'),body.get('discount_pct',0),body.get('tax_pct',14),body.get('currency','EGP')))
            return self.reply({'ok':False,'error':'Unknown endpoint'},404)
        except PermissionError as e: return self.reply({'ok':False,'error':str(e)},403)
        except ValueError as e: return self.reply({'ok':False,'error':str(e)},400)
        except sqlite3.Error: return self.reply({'ok':False,'error':'تعذرت معالجة العملية في قاعدة البيانات'},500)

    def log_message(self,fmt,*args):
        pass


if __name__=='__main__':
    if not DB_PATH.is_file(): raise SystemExit('SQLite file missing: '+str(DB_PATH))
    print('UES Desktop (authenticated local demo) listening on http://127.0.0.1:'+str(PORT),flush=True)
    HTTPServer((HOST,PORT),Handler).serve_forever()
