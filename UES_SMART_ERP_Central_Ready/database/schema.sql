-- =============================================================================
-- UES SMART ERP — UNITED EDUCATIONAL SERVICES (المتحدة للخدمات التعليمية)
-- Complete Enterprise Database Schema (PostgreSQL / SQLite Compatible DDL)
-- Covers all 36 core entities required in Section 28
-- =============================================================================

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organizations (
  id TEXT PRIMARY KEY,
  name_ar TEXT NOT NULL,
  name_en TEXT NOT NULL,
  slogan_ar TEXT DEFAULT 'UES | المتحدة للخدمات التعليمية',
  slogan_en TEXT DEFAULT 'One Intelligent Platform. Complete Business Control.',
  default_currency TEXT NOT NULL DEFAULT 'EGP',
  tax_rate_bps INTEGER NOT NULL DEFAULT 1400, -- 14.00%
  max_auto_discount_pct REAL NOT NULL DEFAULT 10.0,
  email TEXT,
  phone TEXT,
  address TEXT,
  legal_info TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS roles (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  code TEXT NOT NULL UNIQUE,
  name_ar TEXT NOT NULL,
  name_en TEXT NOT NULL,
  description TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS permissions (
  id TEXT PRIMARY KEY,
  role_id TEXT NOT NULL REFERENCES roles(id),
  resource TEXT NOT NULL,
  action TEXT NOT NULL,
  allowed INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role_code TEXT NOT NULL,
  is_owner INTEGER NOT NULL DEFAULT 0,
  is_active INTEGER NOT NULL DEFAULT 1,
  mfa_enabled INTEGER NOT NULL DEFAULT 0,
  failed_attempts INTEGER NOT NULL DEFAULT 0,
  locked_until TEXT,
  last_login_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS profiles (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE REFERENCES users(id),
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  full_name TEXT NOT NULL,
  department TEXT NOT NULL,
  job_title TEXT NOT NULL,
  phone TEXT,
  academic_specialization TEXT,
  skills_json TEXT DEFAULT '[]',
  work_capacity INTEGER NOT NULL DEFAULT 8,
  availability_status TEXT NOT NULL DEFAULT 'available',
  avatar_initials TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS memberships (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  user_id TEXT NOT NULL REFERENCES users(id),
  role_id TEXT NOT NULL REFERENCES roles(id),
  status TEXT NOT NULL DEFAULT 'active',
  joined_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS invitations (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  email TEXT NOT NULL,
  full_name TEXT NOT NULL,
  role_code TEXT NOT NULL,
  department TEXT NOT NULL,
  token TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'pending', -- pending, accepted, expired, revoked
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS contacts (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  full_name TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT,
  country TEXT NOT NULL,
  city TEXT,
  university TEXT,
  faculty TEXT,
  academic_degree TEXT NOT NULL, -- بكالوريوس، ماجستير، دكتوراه، باحث مستقل
  research_field TEXT,
  preferred_language TEXT DEFAULT 'ar',
  preferred_channel TEXT DEFAULT 'WhatsApp',
  source TEXT NOT NULL,
  priority TEXT DEFAULT 'متوسطة',
  customer_status TEXT DEFAULT 'نشط',
  lifetime_value_cents INTEGER DEFAULT 0,
  assigned_sales_id TEXT REFERENCES users(id),
  marketing_consent INTEGER DEFAULT 1,
  ai_processing_consent INTEGER DEFAULT 1,
  tags_json TEXT DEFAULT '[]',
  notes TEXT,
  merged_into_id TEXT,
  is_archived INTEGER DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS contact_identities (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  channel_type TEXT NOT NULL,
  external_identifier TEXT NOT NULL,
  is_verified INTEGER NOT NULL DEFAULT 0,
  merge_review_status TEXT DEFAULT 'verified', -- verified, pending_review, rejected
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS channels (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  provider_code TEXT NOT NULL, -- whatsapp, messenger, instagram, telegram, webchat, email
  api_type TEXT NOT NULL,
  connection_status TEXT NOT NULL DEFAULT 'disconnected', -- disconnected, testing, connected, error
  account_identifier TEXT,
  webhook_health TEXT DEFAULT 'unconfigured',
  last_event_at TEXT,
  last_error TEXT,
  limitations_note TEXT,
  ai_enabled INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  channel_id TEXT NOT NULL REFERENCES channels(id),
  channel_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'مفتوحة', -- مفتوحة، انتظار الموظف، بانتظار العميل، بانتظار الاعتماد، مغلقة
  priority TEXT NOT NULL DEFAULT 'متوسطة',
  unread_count INTEGER NOT NULL DEFAULT 0,
  assigned_to TEXT REFERENCES users(id),
  handling_mode TEXT NOT NULL DEFAULT 'AI', -- AI, Human
  tags_json TEXT DEFAULT '[]',
  handoff_history_json TEXT DEFAULT '[]',
  last_message_text TEXT,
  last_message_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  conversation_id TEXT NOT NULL REFERENCES conversations(id),
  sender_type TEXT NOT NULL, -- customer, ai, staff, internal_note
  sender_name TEXT NOT NULL,
  body TEXT NOT NULL,
  message_type TEXT DEFAULT 'text', -- text, quote_card, contract_card, file, audio
  related_entity_id TEXT,
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS message_attachments (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  message_id TEXT NOT NULL REFERENCES messages(id),
  file_name TEXT NOT NULL,
  mime_type TEXT NOT NULL,
  file_size_bytes INTEGER NOT NULL,
  storage_path TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS leads (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  service_id TEXT,
  title TEXT NOT NULL,
  stage TEXT NOT NULL DEFAULT 'عميل محتمل جديد', -- عميل محتمل جديد، تم التواصل، مؤهل، تم جمع المتطلبات، تم إعداد العرض، تم إرسال العرض، تفاوض، مكتسب، مفقود
  lost_reason TEXT,
  estimated_value_cents INTEGER NOT NULL DEFAULT 0,
  currency TEXT NOT NULL DEFAULT 'EGP',
  lead_score INTEGER NOT NULL DEFAULT 60,
  priority TEXT NOT NULL DEFAULT 'متوسطة',
  assigned_to TEXT REFERENCES users(id),
  last_contact_at TEXT,
  next_followup_at TEXT,
  target_delivery_date TEXT,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS lead_activities (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  lead_id TEXT NOT NULL REFERENCES leads(id),
  activity_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS service_categories (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  code TEXT NOT NULL,
  name_ar TEXT NOT NULL,
  name_en TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS services (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  service_code TEXT NOT NULL UNIQUE,
  category_id TEXT NOT NULL REFERENCES service_categories(id),
  category_name_ar TEXT NOT NULL,
  name_ar TEXT NOT NULL,
  name_en TEXT NOT NULL,
  description TEXT NOT NULL,
  deliverables TEXT NOT NULL,
  scope TEXT NOT NULL,
  required_documents TEXT NOT NULL,
  base_price_cents INTEGER NOT NULL, -- Stored in cents/piastres with DEMO label
  pricing_method TEXT NOT NULL, -- Fixed Price, Price per Page, Price per Word, Price per Hour, Price per Service Package, Price per Statistical Analysis
  currency TEXT NOT NULL DEFAULT 'EGP',
  min_duration_days INTEGER NOT NULL DEFAULT 5,
  estimated_hours INTEGER NOT NULL DEFAULT 12,
  assigned_department TEXT NOT NULL,
  revision_policy TEXT NOT NULL DEFAULT 'مراجعتان مجانيتان خلال 14 يوماً ضمن النطاق المتفق عليه',
  availability_status TEXT NOT NULL DEFAULT 'متاحة',
  is_demo_price INTEGER NOT NULL DEFAULT 1,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS pricing_rules (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  rule_name TEXT NOT NULL,
  rule_type TEXT NOT NULL, -- complexity, urgency, academic_level, exchange_rate, discount_limit
  key_code TEXT NOT NULL,
  multiplier_or_rate REAL NOT NULL,
  source_note TEXT,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS quotes (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  quote_number TEXT NOT NULL UNIQUE,
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  lead_id TEXT REFERENCES leads(id),
  service_id TEXT REFERENCES services(id),
  title TEXT NOT NULL,
  description TEXT,
  pricing_method TEXT NOT NULL DEFAULT 'Fixed Price',
  quantity INTEGER NOT NULL DEFAULT 1,
  unit_price_cents INTEGER NOT NULL,
  complexity_level TEXT NOT NULL DEFAULT 'قياسي',
  complexity_multiplier REAL NOT NULL DEFAULT 1.0,
  urgency_level TEXT NOT NULL DEFAULT 'عادي',
  urgency_multiplier REAL NOT NULL DEFAULT 1.0,
  academic_level TEXT NOT NULL DEFAULT 'دكتوراه',
  academic_multiplier REAL NOT NULL DEFAULT 1.0,
  discount_pct REAL NOT NULL DEFAULT 0,
  discount_cents INTEGER NOT NULL DEFAULT 0,
  tax_pct REAL NOT NULL DEFAULT 14.0,
  tax_cents INTEGER NOT NULL DEFAULT 0,
  total_cents INTEGER NOT NULL,
  estimated_cost_cents INTEGER NOT NULL DEFAULT 0,
  currency TEXT NOT NULL DEFAULT 'EGP',
  proposed_duration_days INTEGER NOT NULL DEFAULT 7,
  delivery_terms TEXT,
  revision_policy TEXT,
  payment_terms TEXT DEFAULT '30% تعاقد - 30% مرحلة أولى - 30% مرحلة ثانية - 10% تسليم نهائي',
  valid_until TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'مسودة', -- مسودة، بانتظار الاعتماد، معتمد، مرسل، مقبول، مرفوض، منتهي الصلاحية
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS quote_items (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  quote_id TEXT NOT NULL REFERENCES quotes(id),
  service_id TEXT REFERENCES services(id),
  item_name TEXT NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  unit_price_cents INTEGER NOT NULL,
  line_total_cents INTEGER NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quote_approvals (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  quote_id TEXT NOT NULL REFERENCES quotes(id),
  requested_by TEXT NOT NULL,
  decided_by TEXT,
  decision TEXT NOT NULL DEFAULT 'pending', -- pending, approved, rejected
  notes TEXT,
  decided_at TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quote_acceptances (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  quote_id TEXT NOT NULL REFERENCES quotes(id),
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  acceptance_method TEXT NOT NULL,
  snapshot_total_cents INTEGER NOT NULL,
  accepted_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS contracts (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  contract_number TEXT NOT NULL UNIQUE,
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  quote_id TEXT NOT NULL REFERENCES quotes(id),
  title TEXT NOT NULL,
  contract_value_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'EGP',
  scope_of_work TEXT NOT NULL,
  deliverables TEXT NOT NULL,
  start_date TEXT NOT NULL,
  agreed_deadline TEXT NOT NULL,
  installments_json TEXT NOT NULL DEFAULT '[30,30,30,10]',
  revision_terms TEXT NOT NULL,
  confidentiality_terms TEXT NOT NULL,
  cancellation_terms TEXT NOT NULL,
  template_lang TEXT NOT NULL DEFAULT 'ar',
  approval_status TEXT NOT NULL DEFAULT 'معتمد',
  signature_status TEXT NOT NULL DEFAULT 'مسودة بانتظار التوقيع', -- مسودة بانتظار التوقيع، موافقة مسجلة (محاكاة)، موقع عبر مزود معتمد
  signed_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS contract_milestones (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  contract_id TEXT NOT NULL REFERENCES contracts(id),
  milestone_order INTEGER NOT NULL,
  title TEXT NOT NULL,
  percentage REAL NOT NULL,
  amount_cents INTEGER NOT NULL,
  due_date TEXT,
  status TEXT NOT NULL DEFAULT 'مجدول',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  project_code TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  contract_id TEXT REFERENCES contracts(id),
  manager_id TEXT REFERENCES users(id),
  academic_department TEXT NOT NULL,
  assigned_team_json TEXT DEFAULT '[]',
  start_date TEXT NOT NULL,
  deadline TEXT NOT NULL,
  current_stage TEXT NOT NULL DEFAULT 'التخطيط', -- لم يبدأ، التخطيط، قيد التنفيذ، مراجعة داخلية، مراجعة الباحث، مطلوب تعديلات، جاهز للتسليم، مكتمل، معلق، ملغى
  progress_pct INTEGER NOT NULL DEFAULT 0,
  budget_cents INTEGER NOT NULL DEFAULT 0,
  internal_cost_cents INTEGER NOT NULL DEFAULT 0,
  currency TEXT NOT NULL DEFAULT 'EGP',
  priority TEXT NOT NULL DEFAULT 'متوسطة',
  client_notes TEXT,
  internal_notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS project_members (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  project_id TEXT NOT NULL REFERENCES projects(id),
  user_id TEXT NOT NULL REFERENCES users(id),
  role_in_project TEXT NOT NULL,
  assigned_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  task_code TEXT NOT NULL UNIQUE,
  project_id TEXT NOT NULL REFERENCES projects(id),
  title TEXT NOT NULL,
  description TEXT,
  assigned_to TEXT NOT NULL REFERENCES users(id),
  start_date TEXT NOT NULL,
  due_date TEXT NOT NULL,
  priority TEXT NOT NULL DEFAULT 'متوسطة',
  status TEXT NOT NULL DEFAULT 'قيد الانتظار', -- قيد الانتظار، قيد التنفيذ، قيد المراجعة، مطلوب تعديل، مكتملة، متوقفة
  progress_pct INTEGER NOT NULL DEFAULT 0,
  estimated_hours REAL NOT NULL DEFAULT 4,
  actual_hours REAL NOT NULL DEFAULT 0,
  review_status TEXT NOT NULL DEFAULT 'بانتظار المراجعة',
  checklist_json TEXT DEFAULT '[]',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS task_comments (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  task_id TEXT NOT NULL REFERENCES tasks(id),
  author_id TEXT NOT NULL REFERENCES users(id),
  author_name TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS team_availability (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  user_id TEXT NOT NULL REFERENCES users(id),
  available_hours_weekly INTEGER NOT NULL DEFAULT 40,
  allocated_hours_weekly INTEGER NOT NULL DEFAULT 16,
  next_available_slot TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  invoice_number TEXT NOT NULL UNIQUE,
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  contract_id TEXT REFERENCES contracts(id),
  milestone_title TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  tax_cents INTEGER NOT NULL DEFAULT 0,
  paid_cents INTEGER NOT NULL DEFAULT 0,
  remaining_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'EGP',
  due_date TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'صادرة', -- مسودة، صادرة، مدفوعة جزئياً، مدفوعة، متأخرة، ملغاة
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS payments (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  payment_number TEXT NOT NULL UNIQUE,
  invoice_id TEXT NOT NULL REFERENCES invoices(id),
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'EGP',
  payment_method TEXT NOT NULL, -- Bank Transfer, InstaPay, Vodafone Cash, Payment Gateway, Cash, Other Approved Method
  reference_number TEXT NOT NULL UNIQUE, -- Enforces idempotency / duplicate prevention
  proof_document TEXT,
  verification_source TEXT NOT NULL, -- finance_officer, verified_webhook
  verified_by TEXT NOT NULL,
  paid_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS expenses (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  project_id TEXT REFERENCES projects(id),
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'EGP',
  expense_date TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  agent_name TEXT NOT NULL DEFAULT 'UES Academic Business Assistant',
  provider TEXT NOT NULL DEFAULT 'google_gemini', -- google_gemini, openai
  model_name TEXT NOT NULL DEFAULT 'gemini-2.5-pro',
  connection_mode TEXT NOT NULL DEFAULT 'غير متصل — وضع تجريبي',
  system_instructions TEXT NOT NULL,
  response_language TEXT NOT NULL DEFAULT 'ar_multi_dialect',
  response_tone TEXT NOT NULL DEFAULT 'أكاديمي استشاري رصين',
  max_discount_pct REAL NOT NULL DEFAULT 10.0,
  confidence_threshold REAL NOT NULL DEFAULT 0.80,
  system_enabled INTEGER NOT NULL DEFAULT 1,
  allowed_tools_json TEXT NOT NULL,
  business_hours TEXT NOT NULL DEFAULT '09:00 - 22:00 بتوقيت القاهرة',
  token_usage_count INTEGER NOT NULL DEFAULT 14250,
  estimated_cost_usd REAL NOT NULL DEFAULT 0.00,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS knowledge_documents (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  source_file_name TEXT NOT NULL,
  file_type TEXT NOT NULL, -- PDF, DOCX, TXT, CSV, XLSX
  version_number TEXT NOT NULL DEFAULT 'v1.0',
  extracted_text TEXT NOT NULL,
  approval_status TEXT NOT NULL DEFAULT 'معتمد', -- مسودة، معتمد، مؤرشف
  is_client_uploaded INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS ai_conversation_runs (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  scenario_code TEXT,
  user_input TEXT NOT NULL,
  detected_intent TEXT NOT NULL,
  invoked_tool TEXT NOT NULL,
  tool_output_summary TEXT NOT NULL,
  ai_response TEXT NOT NULL,
  risk_level TEXT NOT NULL DEFAULT 'منخفض',
  requires_human_approval INTEGER NOT NULL DEFAULT 0,
  mode_label TEXT NOT NULL DEFAULT 'غير متصل — وضع تجريبي',
  created_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS automation_rules (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  title TEXT NOT NULL,
  trigger_event TEXT NOT NULL,
  condition_expr TEXT NOT NULL,
  action_type TEXT NOT NULL,
  responsible_user_id TEXT REFERENCES users(id),
  requires_approval INTEGER NOT NULL DEFAULT 0,
  is_enabled INTEGER NOT NULL DEFAULT 1,
  run_count INTEGER NOT NULL DEFAULT 0,
  last_run_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS automation_runs (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  rule_id TEXT NOT NULL REFERENCES automation_rules(id),
  idempotency_key TEXT NOT NULL UNIQUE,
  event_summary TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'نجاح', -- نجاح، فشل، بانتظار الموافقة
  result_note TEXT NOT NULL,
  executed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  notification_type TEXT NOT NULL,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  priority TEXT NOT NULL DEFAULT 'متوسطة',
  is_read INTEGER NOT NULL DEFAULT 0,
  target_page TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  request_type TEXT NOT NULL, -- اعتماد عرض سعر، خصم استثنائي، اعتماد عقد، تحقق دفعة، تصعيد AI
  related_entity_id TEXT NOT NULL,
  requester_name TEXT NOT NULL,
  client_name TEXT NOT NULL,
  amount_display TEXT NOT NULL,
  reason TEXT NOT NULL,
  assigned_approver TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'قيد الانتظار', -- قيد الانتظار، معتمد، مرفوض، منتهي
  decided_by TEXT,
  decision_notes TEXT,
  requested_at TEXT NOT NULL,
  decided_at TEXT
);

CREATE TABLE IF NOT EXISTS files (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  file_name TEXT NOT NULL,
  category TEXT NOT NULL, -- Research Documents, Questionnaires, Statistical Data, Contracts, Invoices, Deliverables, Reviewer Comments, Revision Files, Internal Documents
  mime_type TEXT NOT NULL,
  size_kb INTEGER NOT NULL,
  version_label TEXT NOT NULL DEFAULT 'v1.0',
  project_id TEXT REFERENCES projects(id),
  contact_id TEXT REFERENCES contacts(id),
  access_level TEXT NOT NULL DEFAULT 'فريق المشروع والباحث', -- داخلي سري، فريق المشروع فقط، فريق المشروع والباحث
  is_archived INTEGER NOT NULL DEFAULT 0,
  signed_url_expiry_mins INTEGER NOT NULL DEFAULT 15,
  content_preview TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_by TEXT
);

CREATE TABLE IF NOT EXISTS settings (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  category TEXT NOT NULL,
  setting_key TEXT NOT NULL,
  setting_value TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS activity_logs (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  actor_name TEXT NOT NULL,
  actor_role TEXT NOT NULL,
  category TEXT NOT NULL,
  action_summary TEXT NOT NULL,
  entity_type TEXT,
  entity_id TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS webhook_events (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  channel_provider TEXT NOT NULL,
  external_event_id TEXT NOT NULL UNIQUE,
  signature_valid INTEGER NOT NULL DEFAULT 1,
  processing_status TEXT NOT NULL DEFAULT 'processed',
  payload_summary TEXT NOT NULL,
  received_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS integration_connections (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  channel_id TEXT NOT NULL REFERENCES channels(id),
  secret_ref_name TEXT NOT NULL,
  webhook_url TEXT NOT NULL,
  verified_at TEXT,
  status TEXT NOT NULL DEFAULT 'awaiting_credentials',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS client_portal_access (
  id TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  contact_id TEXT NOT NULL UNIQUE REFERENCES contacts(id),
  portal_email TEXT NOT NULL,
  access_status TEXT NOT NULL DEFAULT 'مفعل',
  last_accessed_at TEXT,
  allowed_sections_json TEXT NOT NULL DEFAULT '["profile","services","contracts","quotes","projects","files","invoices","installments","revisions","support","notifications"]',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_contacts_org ON contacts(organization_id, phone, email);
CREATE INDEX IF NOT EXISTS idx_leads_org_stage ON leads(organization_id, stage);
CREATE INDEX IF NOT EXISTS idx_quotes_org_status ON quotes(organization_id, status);
CREATE INDEX IF NOT EXISTS idx_projects_org_stage ON projects(organization_id, current_stage);
CREATE INDEX IF NOT EXISTS idx_tasks_project_assigned ON tasks(project_id, assigned_to, status);
CREATE INDEX IF NOT EXISTS idx_invoices_contact_status ON invoices(contact_id, status);
CREATE INDEX IF NOT EXISTS idx_activity_logs_created ON activity_logs(organization_id, created_at DESC);
