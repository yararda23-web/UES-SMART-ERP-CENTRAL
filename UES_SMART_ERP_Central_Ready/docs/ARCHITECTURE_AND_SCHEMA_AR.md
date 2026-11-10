# وثيقة المعمارية ومخطط قاعدة البيانات (Architecture & Database Schema)

## 1. البنية المعمارية (System Architecture)
يتكون النظام من 4 طبقات مترابطة:
1. **طبقة العرض والديسكتوب (`Electron + Tailwind RTL/LTR SPA`):** توفر الأقسام الـ 27 بالكامل مع بوابة الباحث وشريط عنوان الديسكتوب ودعم الوضع الليلي والنهاري.
2. **طبقة الخدمات ومنطق الأعمال الخادمي (`backend/src/server.py` & `http_server.py`):** تنفذ التحقق من الصلاحيات `RBAC`، معادلات التسعير الدقيقة بالـ Cents، التحقق من نسب العقود (100%)، ومنع تكرار الدفعات `Idempotency`.
3. **طبقة الذكاء الاصطناعي المحكوم (`AI Agent & RAG Engine`):** تربط الوكيل `UES Academic Business Assistant` بـ 14 أداة خادمية وبقاعدة المعرفة المعتمدة فقط، وتعرض حالة الاتصال الحقيقية (`غير متصل — وضع تجريبي` عند عدم وجود مفاتيح).
4. **طبقة قاعدة البيانات الدائمة (`database/schema.sql` & `ues_smart_erp.db`):** تضم 45 جدولاً مترابطاً بمفاتيح أجنبية وفهارس بحث وحقول تدقيق (`id, organization_id, created_at, updated_at, created_by`).

## 2. الجداول الأساسية المنفذة (45 جدولاً)
تشمل الجداول المنفذة في `database/schema.sql`:
`organizations`, `roles`, `permissions`, `users`, `profiles`, `memberships`, `invitations`, `contacts`, `contact_identities`, `channels`, `conversations`, `messages`, `message_attachments`, `leads`, `lead_activities`, `service_categories`, `services`, `pricing_rules`, `quotes`, `quote_items`, `quote_approvals`, `quote_acceptances`, `contracts`, `contract_milestones`, `projects`, `project_members`, `tasks`, `task_comments`, `team_availability`, `invoices`, `payments`, `expenses`, `agents`, `knowledge_documents`, `ai_conversation_runs`, `automation_rules`, `automation_runs`, `notifications`, `approvals`, `files`, `settings`, `activity_logs`, `webhook_events`, `integration_connections`, `client_portal_access`.
