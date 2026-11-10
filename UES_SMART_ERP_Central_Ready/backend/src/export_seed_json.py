#!/usr/bin/env python3
"""
Exports all 36 SQLite tables from ues_smart_erp.db into a clean JSON snapshot
so the interactive Desktop/Canvas frontend initializes directly from the verified relational database.
"""
import sqlite3
import json
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../database/ues_smart_erp.db"))
OUT_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src/db_snapshot.json"))

TABLES = [
    "organizations", "roles", "permissions", "users", "profiles", "memberships", "invitations",
    "contacts", "contact_identities", "channels", "conversations", "messages", "message_attachments",
    "leads", "lead_activities", "service_categories", "services", "pricing_rules",
    "quotes", "quote_items", "quote_approvals", "quote_acceptances",
    "contracts", "contract_milestones", "projects", "project_members", "tasks", "task_comments",
    "team_availability", "invoices", "payments", "expenses",
    "agents", "knowledge_documents", "ai_conversation_runs",
    "automation_rules", "automation_runs", "notifications", "approvals", "files",
    "settings", "activity_logs", "webhook_events", "integration_connections", "client_portal_access"
]

def export_all():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    data = {}
    for t in TABLES:
        rows = conn.execute(f"SELECT * FROM {t}").fetchall()
        data[t] = [dict(r) for r in rows]
    conn.close()
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(TABLES)} tables to {OUT_JSON} ({os.path.getsize(OUT_JSON)} bytes)")

if __name__ == "__main__":
    export_all()
