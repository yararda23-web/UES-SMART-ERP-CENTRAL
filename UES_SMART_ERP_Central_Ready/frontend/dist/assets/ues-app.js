(function(){
'use strict';
const SEED_DB = {"organizations": [], "roles": [], "permissions": [], "users": [], "profiles": [], "memberships": [], "invitations": [], "contacts": [], "contact_identities": [], "channels": [], "conversations": [], "messages": [], "message_attachments": [], "leads": [], "lead_activities": [], "service_categories": [], "services": [], "pricing_rules": [], "quotes": [], "quote_items": [], "quote_approvals": [], "quote_acceptances": [], "contracts": [], "contract_milestones": [], "projects": [], "project_members": [], "tasks": [], "task_comments": [], "team_availability": [], "invoices": [], "payments": [], "expenses": [], "agents": [], "knowledge_documents": [], "ai_conversation_runs": [], "automation_rules": [], "automation_runs": [], "notifications": [], "approvals": [], "files": [], "settings": [], "activity_logs": [], "webhook_events": [], "integration_connections": [], "client_portal_access": []};

  // ============================================================================
  // UES SMART ERP — Core Database Engine, RBAC, Navigation & Helpers
  // ============================================================================
  const NAV_ITEMS = [
    { id: 'dashboard', num: 1, group: 'القيادة والتحكم', ar: 'لوحة التحكم الرئيسية', en: 'Main Dashboard', icon: '📊', perm: 'view_dashboard' },
    { id: 'inbox', num: 2, group: 'التواصل والعملاء', ar: 'صندوق الرسائل الموحد', en: 'Unified Inbox', icon: '💬', perm: 'inbox' },
    { id: 'contacts', num: 3, group: 'التواصل والعملاء', ar: 'العملاء', en: 'Contacts / CRM', icon: '👥', perm: 'contacts' },
    { id: 'leads', num: 4, group: 'التواصل والعملاء', ar: 'العملاء المحتملون', en: 'Leads Management', icon: '🎯', perm: 'leads' },
    { id: 'pipeline', num: 5, group: 'التواصل والعملاء', ar: 'مسار المبيعات', en: 'Sales Pipeline (Kanban)', icon: '🗂️', perm: 'leads' },
    { id: 'catalog', num: 6, group: 'العمليات التجارية', ar: 'الخدمات الأكاديمية', en: 'Academic Service Catalog', icon: '🎓', perm: 'catalog' },
    { id: 'pricing', num: 7, group: 'العمليات التجارية', ar: 'التسعير الذكي', en: 'Smart Pricing Engine', icon: '🧮', perm: 'pricing' },
    { id: 'quotes', num: 8, group: 'العمليات التجارية', ar: 'عروض الأسعار', en: 'Quotations', icon: '📄', perm: 'quotes' },
    { id: 'contracts', num: 9, group: 'العمليات التجارية', ar: 'العقود والاتفاقيات', en: 'Contracts & Agreements', icon: '🖋️', perm: 'contracts' },
    { id: 'projects', num: 10, group: 'إدارة المشروعات ERP', ar: 'المشروعات', en: 'Projects ERP', icon: '🚀', perm: 'projects' },
    { id: 'tasks', num: 11, group: 'إدارة المشروعات ERP', ar: 'المهام والمتابعة', en: 'Tasks & Follow-up', icon: '✅', perm: 'tasks' },
    { id: 'timeline', num: 12, group: 'إدارة المشروعات ERP', ar: 'الجدول الزمني', en: 'Timeline & Schedule', icon: '📅', perm: 'projects' },
    { id: 'team', num: 13, group: 'إدارة المشروعات ERP', ar: 'فريق العمل', en: 'Team & Capacity', icon: '🧑‍🏫', perm: 'team' },
    { id: 'invoices', num: 14, group: 'المالية والمحاسبة', ar: 'الفواتير', en: 'Invoices', icon: '🧾', perm: 'finance' },
    { id: 'payments', num: 15, group: 'المالية والمحاسبة', ar: 'المدفوعات والأقساط', en: 'Payments & Installments', icon: '💳', perm: 'finance' },
    { id: 'reports', num: 16, group: 'المالية والمحاسبة', ar: 'التقارير والتحليلات', en: 'Reports & BI', icon: '📈', perm: 'reports' },
    { id: 'ai_center', num: 17, group: 'الذكاء والأتمتة', ar: 'مركز الذكاء الاصطناعي', en: 'AI Agent Center', icon: '🤖', perm: 'ai' },
    { id: 'knowledge', num: 18, group: 'الذكاء والأتمتة', ar: 'قاعدة المعرفة', en: 'Knowledge Base & RAG', icon: '📚', perm: 'ai' },
    { id: 'automation', num: 19, group: 'الذكاء والأتمتة', ar: 'الأتمتة', en: 'Automation Workflows', icon: '⚡', perm: 'automation' },
    { id: 'integrations', num: 20, group: 'الذكاء والأتمتة', ar: 'ربط منصات التواصل', en: 'Channel Integrations', icon: '🔗', perm: 'integrations' },
    { id: 'portal', num: 21, group: 'البوابات والمستندات', ar: 'بوابة الباحث', en: 'Client Portal', icon: '🏛️', perm: 'portal' },
    { id: 'files', num: 22, group: 'البوابات والمستندات', ar: 'الملفات والمستندات', en: 'Files & Documents', icon: '📁', perm: 'files' },
    { id: 'notifications', num: 23, group: 'الحوكمة والإدارة', ar: 'الإشعارات', en: 'Notifications Center', icon: '🔔', perm: 'notifications' },
    { id: 'approvals', num: 24, group: 'الحوكمة والإدارة', ar: 'الموافقات الإدارية', en: 'Executive Approvals', icon: '🛡️', perm: 'approvals' },
    { id: 'audit', num: 25, group: 'الحوكمة والإدارة', ar: 'سجل النشاط والتدقيق', en: 'Audit & Activity Log', icon: '📜', perm: 'audit' },
    { id: 'settings', num: 26, group: 'الحوكمة والإدارة', ar: 'الإعدادات', en: 'System Settings', icon: '⚙️', perm: 'settings' },
    { id: 'rbac', num: 27, group: 'الحوكمة والإدارة', ar: 'إدارة المستخدمين والصلاحيات', en: 'Users & RBAC', icon: '🔐', perm: 'rbac' }
  ];

  const ROLE_MATRIX = {
    super_admin: { label: 'Super Admin / Owner (مالك النظام)', allowed: ['*'] },
    general_manager: { label: 'General Manager (المدير العام)', allowed: ['view_dashboard','inbox','contacts','leads','catalog','pricing','quotes','contracts','projects','tasks','team','reports','ai','knowledge','automation','portal','files','notifications','approvals','audit'] },
    sales_manager: { label: 'Sales Manager (مدير المبيعات)', allowed: ['view_dashboard','inbox','contacts','leads','catalog','pricing','quotes','contracts','reports','notifications','approvals'] },
    sales_rep: { label: 'Sales Representative (ممثل مبيعات)', allowed: ['view_dashboard','inbox','contacts','leads','catalog','pricing','quotes','notifications'] },
    academic_manager: { label: 'Academic Operations Manager (مدير أكاديمي)', allowed: ['view_dashboard','catalog','projects','tasks','team','knowledge','files','notifications'] },
    academic_specialist: { label: 'Academic Specialist (أخصائي أكاديمي)', allowed: ['view_dashboard','projects','tasks','files','notifications'] },
    finance_manager: { label: 'Finance Manager (مدير الماليّة)', allowed: ['view_dashboard','contracts','invoices','payments','reports','notifications','approvals'] },
    customer_support: { label: 'Customer Support (خدمة العملاء)', allowed: ['view_dashboard','inbox','contacts','leads','notifications'] },
    viewer: { label: 'Viewer (مراقب قراءة فقط)', allowed: ['view_dashboard','reports'] },
    client: { label: 'Client (باحث — بوابة الباحث فقط)', allowed: ['portal'] }
  };

  const LOGIN_PORTALS = {
    owner: {
      id: 'owner',
      title: 'بوابة دخول المالك والأدمن (Owner / Super Admin Portal)',
      subtitle: 'صلاحية كاملة لإدارة جميع الأقسام وإنشاء حسابات الموظفين وتحديد صلاحياتهم',
      badge: 'بوابة المالك الحصرية',
      allowedRoles: ['super_admin'],
      defaultUser: 'Ahmed_99',

      accent: 'from-navy-dark via-navy to-teal'
    },
    gm: {
      id: 'gm',
      title: 'بوابة دخول المدير العام (General Manager Portal)',
      subtitle: 'إدارة العمليات والمشروعات والموظفين والتقارير والموافقات الإدارية',
      badge: 'بوابة الإدارة العامة',
      allowedRoles: ['general_manager'],
      defaultUser: 'gm_sherif',

      accent: 'from-slate-900 via-navy-light to-emerald-800'
    },
    sales_manager: {
      id: 'sales_manager',
      title: 'بوابة دخول إدارة المبيعات (Sales Manager Portal)',
      subtitle: 'إدارة فريق المبيعات، عروض الأسعار، العقود، واعتماد الخصومات',
      badge: 'بوابة مدير المبيعات',
      allowedRoles: ['sales_manager'],
      defaultUser: 'sales_mgr_sara',

      accent: 'from-indigo-950 via-navy to-teal'
    },
    sales_rep: {
      id: 'sales_rep',
      title: 'بوابة دخول السيلز وممثلي المبيعات (Sales Representative Portal)',
      subtitle: 'متابعة العملاء، صندوق الرسائل الموحد، الفرص البيعية، وإعداد عروض الأسعار الأولية',
      badge: 'بوابة السيلز (Sales)',
      allowedRoles: ['sales_rep', 'customer_support'],
      defaultUser: 'sales_karim',

      accent: 'from-teal-950 via-navy to-teal'
    },
    other_roles: {
      id: 'other_roles',
      title: 'بوابة الأقسام التخصصية والباحثين (الأكاديمي • المالية • بوابة الباحث)',
      subtitle: 'دخول المختصين الأكاديميين والإحصائيين ومدير المالية والباحثين وفق الدور المسند',
      badge: 'بوابة الأقسام التخصصية',
      allowedRoles: ['academic_manager', 'academic_specialist', 'finance_manager', 'viewer', 'client'],
      defaultUser: 'acad_mgr_reem',

      accent: 'from-navy via-slate-800 to-teal'
    }
  };

  function deepClone(obj) { return JSON.parse(JSON.stringify(obj)); }
  function emptyDatabase() { return deepClone(SEED_DB); }
  let db = emptyDatabase();

  let state = {
    authenticated: false,
    currentUser: null,
    currentProfile: null,
    currentRole: '',
    page: 'dashboard',
    lang: 'ar',
    darkMode: false,
    sidebarCollapsed: false,
    mobileMenuOpen: false,
    searchQuery: '',
    dateRangeFilter: 'all',
    // Inbox state
    selectedConvId: 'CONV-01',
    inboxChannelFilter: 'الكل',
    inboxStatusFilter: 'الكل',
    inboxModeFilter: 'الكل',
    inboxReplyMode: 'staff', // staff or internal_note
    // CRM & Leads state
    contactDegreeFilter: 'الكل',
    leadStageFilter: 'الكل',
    // Projects view mode
    projectViewMode: 'table', // table, kanban, calendar, timeline, gantt
    projectStageFilter: 'الكل',
    // Finance tab
    paymentsTab: 'payments', // payments, installments, receivables, expenses
    // AI Playground
    aiSelectedScenario: 'A',
    aiCustomPrompt: '',
    aiApiKeyConnected: false,
    // Settings tab
    settingsTab: 'Company Profile',
    // Client portal selected client
    portalContactId: 'C-101',
    // Pricing calculator state
    calcContactId: 'C-101',
    calcServiceId: 'SVC-06',
    calcQty: 1,
    calcComplexity: 'متقدم',
    calcUrgency: 'عادي',
    calcAcademic: 'دكتوراه',
    calcDiscountPct: 5,
    calcTaxPct: 14,
    calcCurrency: 'EGP',
    calcDeliveryDate: '2026-11-24',
    // Login screen state
    loginPortalTab: 'owner', // owner, gm, sales_manager, sales_rep, other_roles
    loginUsername: '',
    loginPassword: '',
    showPassword: false,
    mfaCode: '',
    loginError: ''
  };

  function esc(val) {
    return String(val ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  }

  function fmtMoney(cents, currency = 'EGP') {
    const val = (Number(cents) || 0) / 100;
    return `<span class="ltr-num font-bold">${val.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} ${esc(currency)}</span>`;
  }

  function fmtMoneyPlain(cents, currency = 'EGP') {
    const val = (Number(cents) || 0) / 100;
    return `${val.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} ${currency}`;
  }

  function fmtNum(n) {
    return `<span class="ltr-num">${(Number(n) || 0).toLocaleString('en-US')}</span>`;
  }

  function nowStr() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0') + ' ' + String(d.getHours()).padStart(2,'0') + ':' + String(d.getMinutes()).padStart(2,'0') + ':00';
  }

  function uid(prefix) {
    return prefix + '-' + Math.random().toString(36).substring(2, 7).toUpperCase();
  }

  function getContactName(id) {
    const c = db.contacts.find(x => x.id === id);
    return c ? c.full_name : 'غير محدد';
  }

  function getUserName(id) {
    const p = db.profiles.find(x => x.user_id === id);
    if (p) return p.full_name;
    const u = db.users.find(x => x.id === id);
    return u ? u.email : 'غير مسند';
  }

  function getServiceName(id) {
    const s = db.services.find(x => x.id === id);
    return s ? s.name_ar : 'خدمة عامة';
  }

  function hasAccess(perm) {
    if (!state.authenticated || !state.currentUser || state.currentUser.role_code !== state.currentRole) return false;
    // Do not require full roles listing; only owner may download it.
    if (state.currentRole === 'super_admin') return true;
    const r = ROLE_MATRIX[state.currentRole];
    if (!r) return false;
    return r.allowed.includes('*') || r.allowed.includes(perm);
  }

  function canMutate(domain) {
    if (!state.authenticated || !state.currentUser || state.currentUser.role_code !== state.currentRole) return false;
    if (state.currentRole === 'viewer' || state.currentRole === 'client') return false;
    if (state.currentRole === 'super_admin' || state.currentRole === 'general_manager') return true;
    if (domain === 'finance') return state.currentRole === 'finance_manager';
    if (domain === 'approvals') return ['super_admin','general_manager','sales_manager','finance_manager'].includes(state.currentRole);
    if (domain === 'sales') return ['sales_manager','sales_rep','customer_support'].includes(state.currentRole);
    if (domain === 'academic') return ['academic_manager','academic_specialist'].includes(state.currentRole);
    return false;
  }

  function addAuditLog(category, summary, entityType = '', entityId = '') {
    const actor = state.currentProfile ? state.currentProfile.full_name : state.currentUser.email;
    db.activity_logs.unshift({
      id: uid('LOG'),
      organization_id: 'ORG-UES-001',
      actor_name: actor,
      actor_role: state.currentRole,
      category,
      action_summary: summary,
      entity_type: entityType,
      entity_id: entityId,
      created_at: nowStr()
    });
  }

  function showToast(message, type = 'success') {
    const wrap = document.getElementById('toast-container');
    if (!wrap) return;
    const el = document.createElement('div');
    const bg = type === 'error' ? 'bg-red-600 border-red-800' : type === 'warning' ? 'bg-amber-600 border-amber-800' : 'bg-teal border-teal-hover';
    el.className = `pointer-events-auto ${bg} text-white px-4 py-3 rounded-xl shadow-xl border-r-4 text-sm font-semibold flex items-center justify-between gap-3 transition-all`;
    el.innerHTML = `<span>${esc(message)}</span><button class="text-white/80 hover:text-white font-bold" onclick="this.parentElement.remove()">×</button>`;
    wrap.appendChild(el);
    setTimeout(() => { if (el.parentElement) el.remove(); }, 4500);
  }

  function openModal(title, bodyHtml, onSubmitAction = '', wide = false) {
    const container = document.getElementById('modal-container');
    if (!container) return;
    container.innerHTML = `
      <div class="fixed inset-0 bg-navy/75 backdrop-blur-xs z-50 flex items-center justify-center p-4 overflow-y-auto" id="modal-backdrop">
        <div class="surface-card bg-white rounded-2xl shadow-2xl border border-bordercol w-full ${wide ? 'max-w-4xl' : 'max-w-2xl'} overflow-hidden my-8">
          <div class="bg-navy text-white px-6 py-4 flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold">${esc(title)}</h3>
              <p class="text-xs text-slate-300 mt-0.5">UES SMART ERP — المتحدة للخدمات التعليمية</p>
            </div>
            <button data-action="close-modal" class="w-8 h-8 rounded-lg bg-white/10 hover:bg-white/20 flex items-center justify-center text-lg font-bold">×</button>
          </div>
          ${onSubmitAction ? `<form id="dynamic-modal-form" data-submit="${esc(onSubmitAction)}" class="p-6 space-y-4 max-h-[80vh] overflow-y-auto">${bodyHtml}
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-bordercol">
              <button type="button" data-action="close-modal" class="px-4 py-2 rounded-xl border border-bordercol text-sm font-bold hover:bg-slate-100">إلغاء</button>
              <button type="submit" class="px-5 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-sm font-bold shadow">حفظ وتنفيذ</button>
            </div>
          </form>` : `<div class="p-6 space-y-4 max-h-[80vh] overflow-y-auto">${bodyHtml}
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-bordercol">
              <button type="button" data-action="close-modal" class="px-4 py-2 rounded-xl border border-bordercol text-sm font-bold hover:bg-slate-100">إغلاق</button>
            </div>
          </div>`}
        </div>
      </div>
    `;
  }

  function closeModal() {
    const container = document.getElementById('modal-container');
    if (container) container.innerHTML = '';
  }

  function statusBadge(st) {
    const s = String(st || '');
    const green = ['نشط','مفتوحة','مكتسب','مقبول','معتمد','مدفوعة','مكتمل','مكتملة','متاح','متاحة (DEMO)','connected','مفعل','verified','نجاح'];
    const amber = ['بانتظار الاعتماد','تفاوض','انتظار الموظف','بانتظار العميل','قيد التنفيذ','مراجعة داخلية','مدفوعة جزئياً','صادرة','مرسل','قيد الانتظار','قيد المراجعة','متوسط — يتطلب موافقة مدير','متوسط — فحص سعة','متوسط — تحقق مالي','pending_review'];
    const red = ['متأخرة','مرفوض','ملغى','مفقود','متوقفة','مرتفع — حماية نزاهة أكاديمية','مرتفع — تصعيد بشري','disconnected'];
    let cls = 'bg-slate-100 text-slate-700 border-slate-300';
    if (green.includes(s)) cls = 'bg-emerald-50 text-emerald-700 border-emerald-200';
    else if (amber.includes(s)) cls = 'bg-amber-50 text-amber-700 border-amber-200';
    else if (red.includes(s)) cls = 'bg-red-50 text-red-700 border-red-200';
    return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${cls}">${esc(s)}</span>`;
  }

  // Server-equivalent Smart Pricing Engine in JS (Exact Cents Math)
  function computePricing(serviceId, qty, complexityKey, urgencyKey, academicKey, discountPct, taxPct, currency) {
    const svc = db.services.find(s => s.id === serviceId) || db.services[0];
    const getRule = (type, key, def = 1.0) => {
      const r = db.pricing_rules.find(x => x.rule_type === type && x.key_code === key);
      return r ? Number(r.multiplier_or_rate) : def;
    };
    const compM = getRule('complexity', complexityKey, 1.0);
    const urgM = getRule('urgency', urgencyKey, 1.0);
    const acadM = getRule('academic_level', academicKey, 1.0);
    const fxRate = getRule('exchange_rate', currency, 1.0);
    const baseCents = Number(svc.base_price_cents) || 0;
    const quantity = Math.max(1, Number(qty) || 1);
    const grossCents = Math.round(baseCents * quantity * compM * urgM * acadM);
    const dPct = Math.max(0, Math.min(100, Number(discountPct) || 0));
    const discCents = Math.round(grossCents * (dPct / 100));
    const netAfterDisc = grossCents - discCents;
    const tPct = Math.max(0, Number(taxPct) || 0);
    const taxCents = Math.round(netAfterDisc * (tPct / 100));
    const totalEgpCents = netAfterDisc + taxCents;
    const convertedCents = fxRate > 0 ? Math.round(totalEgpCents / fxRate) : totalEgpCents;
    const maxLimit = Number(db.organizations[0]?.max_auto_discount_pct || 10);
    const estCostCents = Math.round((baseCents * quantity * 0.55) / (fxRate > 0 ? fxRate : 1));
    const netConverted = fxRate > 0 ? Math.round(netAfterDisc / fxRate) : netAfterDisc;
    const estMarginCents = netConverted - estCostCents;
    return {
      svc, quantity, compM, urgM, acadM, fxRate,
      baseCents, grossCents, dPct, discCents, tPct, taxCents,
      totalEgpCents, convertedCents, estCostCents, estMarginCents,
      requiresApproval: dPct > maxLimit, maxLimit
    };
  }


  // ============================================================================
  // Shell, Login Screen & Views 1 to 7 (Dashboard, Inbox, Contacts, Leads, Pipeline, Catalog, Pricing)
  // ============================================================================

  function renderLoginScreen() {
    const portal = LOGIN_PORTALS[state.loginPortalTab] || LOGIN_PORTALS.owner;
    // Do not reveal account inventory or passwords to unauthenticated visitors.

    return `
      <div class="min-h-screen bg-gradient-to-br ${portal.accent} flex flex-col justify-between p-5 md:p-8 text-white">
        <div class="flex flex-wrap items-center justify-between max-w-6xl w-full mx-auto gap-3">
          <div class="flex items-center gap-3">
            <div class="w-11 h-11 rounded-2xl bg-teal flex items-center justify-center font-black text-xl shadow-lg">UES</div>
            <div>
              <div class="font-extrabold text-base">المتحدة للخدمات التعليمية — United Educational Services</div>
              <div class="text-xs text-slate-300">UES SMART ERP • بوابات الدخول المخصصة לפי الدور الوظيفي</div>
            </div>
          </div>
          <span class="px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 text-teal-soft text-xs font-extrabold">${esc(portal.badge)}</span>
        </div>

        <!-- Dedicated Login Portals Switcher Bar -->
        <div class="max-w-6xl w-full mx-auto mt-6">
          <div class="text-xs font-bold text-teal-soft mb-2">اختر بوابة تسجيل الدخول المخصصة لدورك الوظيفي:</div>
          <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
            ${[
              ['owner', '👑 دخول المالك (الأدمن)', 'مخصص للمالك'],
              ['gm', '🏛️ دخول المدير العام', 'General Manager'],
              ['sales_manager', '📈 دخول إدارة المبيعات', 'Sales Manager'],
              ['sales_rep', '💼 دخول السيلز (Sales)', 'Sales Rep'],
              ['other_roles', '🎓 الأقسام التخصصية والباحث', 'الأكاديمي / المالية / الباحث']
            ].map(([key, label, sub]) => {
              const active = state.loginPortalTab === key;
              return `
                <button type="button" data-action="switch-login-portal" data-portal="${key}" class="text-right p-3 rounded-2xl border transition ${active ? 'bg-white text-navy border-white shadow-xl font-black' : 'bg-white/10 hover:bg-white/20 border-white/15 text-white'}">
                  <div class="text-xs font-extrabold">${label}</div>
                  <div class="text-[10px] ${active ? 'text-teal font-bold' : 'text-slate-300'} mt-0.5 ltr-num">${sub}</div>
                </button>
              `;
            }).join('')}
          </div>
        </div>

        <div class="max-w-6xl w-full mx-auto grid lg:grid-cols-12 gap-8 items-center my-6">
          <!-- Left Info & Portal Specific Accounts -->
          <div class="lg:col-span-6 space-y-4">
            <span class="inline-block px-3 py-1 rounded-full bg-white/10 text-xs font-bold text-teal-soft">نسخة محلية — الدخول يتطلب اسم مستخدم وكلمة مرور صحيحين</span>
            <h1 class="text-2xl md:text-3xl font-black leading-tight">${esc(portal.title)}</h1>
            <p class="text-slate-200 text-xs md:text-sm leading-relaxed">${esc(portal.subtitle)}</p>

            <div class="bg-white/10 border border-white/15 rounded-2xl p-4 text-xs leading-7">
              🔐 ادخل اسم المستخدم وكلمة المرور اللذين عيّنهما مدير النظام. لا تُعرض كلمات المرور أو قائمة الحسابات في شاشة الدخول.
            </div>
          </div>

          <!-- Right Login Card -->
          <div class="lg:col-span-6 bg-white text-darktxt rounded-3xl shadow-2xl p-7 border border-slate-200">
            <div class="flex items-center justify-between mb-5 border-b border-slate-100 pb-4">
              <div>
                <span class="text-[11px] font-extrabold text-teal">${esc(portal.badge)}</span>
                <h2 class="text-xl font-black text-navy mt-0.5">${esc(portal.title)}</h2>
              </div>
              <div class="w-12 h-12 rounded-2xl bg-navy text-white flex items-center justify-center font-black text-lg">UES</div>
            </div>

            ${state.loginError ? `<div class="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-bold">${esc(state.loginError)}</div>` : ''}

            <form id="login-form" class="space-y-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">اسم المستخدم (Username) أو البريد المؤسسي</label>
                <input type="text" name="username" id="login-email-input" value="" autocomplete="username" placeholder="مثال: Ahmed_99" required class="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-bold ltr-num" />
              </div>
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="text-xs font-bold text-slate-700">كلمة المرور (Password)</label>

                </div>
                <input type="password" name="password" id="login-pw-input" value="" autocomplete="current-password" required class="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-bold ltr-num" />
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1">MFA غير مفعّل في النسخة التجريبية</label>
                  <input type="text" name="mfa" value="${esc(state.mfaCode)}" class="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs ltr-num" />
                </div>
                <div class="flex items-end">
                  <button type="button" data-action="forgot-password" class="w-full py-2 px-3 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 hover:bg-slate-50">استعادة كلمة المرور</button>
                </div>
              </div>
              <button type="submit" class="w-full py-3 rounded-xl bg-teal hover:bg-teal-hover text-white font-extrabold text-sm shadow-lg transition">
                تسجيل الدخول إلى ${esc(portal.badge)}
              </button>
            </form>

            <div class="mt-5 pt-4 border-t border-slate-200 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
              <span>بيانات الدخول شخصية وسرية ولا تُعرض داخل الصفحة.</span>
              <button type="button" data-action="test-unauthorized-signup" class="text-red-600 font-bold hover:underline">اختبار منع إنشاء حساب بدون الأدمن</button>
            </div>
          </div>
        </div>

        <div class="text-center text-xs text-slate-300">
          جميع الحقوق محفوظة © 2026 المتحدة للخدمات التعليمية (United Educational Services) — UES SMART ERP
        </div>
      </div>
    `;
  }

  // ============================================================================
  // SECTION 6 — VIEW 1: MAIN DASHBOARD (20 KPIs + 8 Charts + Attention Required)
  // ============================================================================
  function renderDashboard() {
    const totalContacts = db.contacts.filter(c => !c.is_archived).length;
    const newToday = db.contacts.filter(c => String(c.created_at).startsWith('2026-11-10')).length;
    const newMonth = db.contacts.filter(c => String(c.created_at).startsWith('2026-11')).length;
    const totalLeads = db.leads.length;
    const openLeads = db.leads.filter(l => !['مكتسب','مفقود'].includes(l.stage)).length;
    const sentQuotes = db.quotes.filter(q => ['مرسل','مقبول','بانتظار الاعتماد'].includes(q.status)).length;
    const acceptedQuotes = db.quotes.filter(q => q.status === 'مقبول').length;
    const activeContracts = db.contracts.length;
    const activeProjects = db.projects.filter(p => !['مكتمل','ملغى'].includes(p.current_stage)).length;
    const overdueProjects = db.projects.filter(p => !['مكتمل','ملغى'].includes(p.current_stage) && p.deadline < '2026-11-10').length;
    const completedProjects = db.projects.filter(p => p.current_stage === 'مكتمل').length;
    const totalContractValue = db.contracts.reduce((acc, c) => acc + (Number(c.contract_value_cents) || 0), 0);
    const collectedAmount = db.payments.reduce((acc, p) => acc + (Number(p.amount_cents) || 0), 0);
    const remainingReceivables = db.invoices.reduce((acc, i) => acc + (Number(i.remaining_cents) || 0), 0);
    const overdueInvoices = db.invoices.filter(i => i.status === 'متأخرة' || (i.remaining_cents > 0 && i.due_date < '2026-11-10')).length;
    const unreadConvs = db.conversations.reduce((acc, c) => acc + (Number(c.unread_count) || 0), 0);
    const waitingStaffConvs = db.conversations.filter(c => c.status === 'انتظار الموظف').length;
    const avgResponseMins = 4.2;
    const wonLeads = db.leads.filter(l => l.stage === 'مكتسب').length;
    const leadConvRate = totalLeads ? Math.round((wonLeads / totalLeads) * 100) : 0;
    const completedTasks = db.tasks.filter(t => t.status === 'مكتملة').length;
    const taskCompRate = db.tasks.length ? Math.round((completedTasks / db.tasks.length) * 100) : 0;

    const kpis = [
      { label: 'إجمالي العملاء', val: fmtNum(totalContacts), sub: 'باحث مسجل بقاعدة CRM', icon: '👥', nav: 'contacts' },
      { label: 'العملاء الجدد اليوم', val: fmtNum(newToday), sub: 'مسجلون بتاريخ اليوم', icon: '✨', nav: 'contacts' },
      { label: 'العملاء الجدد هذا الشهر', val: fmtNum(newMonth), sub: 'نوفمبر 2026', icon: '📅', nav: 'contacts' },
      { label: 'العملاء المحتملون', val: fmtNum(totalLeads), sub: 'إجمالي الفرص المسجلة', icon: '🎯', nav: 'leads' },
      { label: 'فرص البيع المفتوحة', val: fmtNum(openLeads), sub: 'قيد التأهيل والتفاوض', icon: '🔥', nav: 'pipeline' },
      { label: 'عروض الأسعار المرسلة', val: fmtNum(sentQuotes), sub: 'عروض نشطة', icon: '📤', nav: 'quotes' },
      { label: 'العروض المقبولة', val: fmtNum(acceptedQuotes), sub: 'جاهزة أو محولة لعقود', icon: '✅', nav: 'quotes' },
      { label: 'العقود النشطة', val: fmtNum(activeContracts), sub: 'عقود معتمدة', icon: '🖋️', nav: 'contracts' },
      { label: 'المشروعات النشطة', val: fmtNum(activeProjects), sub: 'قيد التنفيذ والمراجعة', icon: '🚀', nav: 'projects' },
      { label: 'المشروعات المتأخرة', val: fmtNum(overdueProjects), sub: 'تجاوزت الموعد', icon: '⚠️', nav: 'projects' },
      { label: 'المشروعات المكتملة', val: fmtNum(completedProjects), sub: 'تم التسليم النهائي', icon: '🏆', nav: 'projects' },
      { label: 'إجمالي قيمة التعاقدات', val: fmtMoney(totalContractValue), sub: 'قيمة العقود المعتمدة', icon: '💼', nav: 'contracts' },
      { label: 'المبالغ المحصلة', val: fmtMoney(collectedAmount), sub: 'دفعات مؤكدة مالياً', icon: '💰', nav: 'payments' },
      { label: 'المستحقات المتبقية', val: fmtMoney(remainingReceivables), sub: 'أرصدة فواتير مفتوحة', icon: '📊', nav: 'invoices' },
      { label: 'الفواتير المتأخرة', val: fmtNum(overdueInvoices), sub: 'تحتاج متابعة تحصيل', icon: '🚨', nav: 'invoices' },
      { label: 'المحادثات غير المقروءة', val: fmtNum(unreadConvs), sub: 'في الصندوق الموحد', icon: '💬', nav: 'inbox' },
      { label: 'المحادثات المنتظرة لموظف', val: fmtNum(waitingStaffConvs), sub: 'تحتاج تدخل بشري', icon: '🙋', nav: 'inbox' },
      { label: 'متوسط زمن الاستجابة', val: `<span class="ltr-num font-bold">${avgResponseMins} min</span>`, sub: 'مؤشر سرعة الدعم', icon: '⏱️', nav: 'inbox' },
      { label: 'نسبة تحويل العملاء', val: `<span class="ltr-num font-bold">${leadConvRate}%</span>`, sub: 'مكتسب من إجمالي الفرص', icon: '📈', nav: 'reports' },
      { label: 'معدل إنجاز المهام', val: `<span class="ltr-num font-bold">${taskCompRate}%</span>`, sub: `${completedTasks} من ${db.tasks.length} مهام`, icon: '☑️', nav: 'tasks' }
    ];

    const pendingApprovals = db.approvals.filter(a => a.status === 'قيد الانتظار');
    const overdueInvs = db.invoices.filter(i => i.status === 'متأخرة');
    const humanWaitConvs = db.conversations.filter(c => c.status === 'انتظار الموظف');

    const aiConvsCount = db.conversations.filter(c => c.handling_mode === 'AI').length;
    const humanConvsCount = db.conversations.filter(c => c.handling_mode !== 'AI').length;

    return `
      <div class="space-y-6">
        <!-- Top Banner & Complete Journey Action -->
        <div class="bg-gradient-to-l from-navy via-navy-light to-teal rounded-2xl p-6 text-white shadow-lg flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 text-xs font-bold text-teal-soft mb-1">
              <span>UES | المتحدة للخدمات التعليمية</span>
              <span>•</span>
              <span>نسخة محلية للتجربة — حسابات وكلمات المرور المعروضة تجريبية وغير مناسبة لبيانات حقيقية.</span>
            </div>
            <h1 class="text-2xl font-black">لوحة التحكم القيادية الشاملة (Executive ERP & CRM Command Center)</h1>
            <p class="text-xs text-slate-200 mt-1">جميع المؤشرات الـ 20 والرسوم البيانية الـ 8 محسوبة لحظياً من قاعدة البيانات الفعلية للنظام.</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <select data-action="change-date-range" class="bg-white/10 border border-white/20 text-white text-xs rounded-xl px-3 py-2 font-bold">
              <option value="all" ${state.dateRangeFilter==='all'?'selected':''}>الفترة: كل السجلات (نوفمبر 2026)</option>
              <option value="today" ${state.dateRangeFilter==='today'?'selected':''}>اليوم (10 نوفمبر 2026)</option>
              <option value="month" ${state.dateRangeFilter==='month'?'selected':''}>هذا الشهر</option>
            </select>
            <button data-action="run-full-journey" class="px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-navy font-black text-xs shadow-lg transition flex items-center gap-1.5">
              <span>⚡ تشغيل رحلة الباحث الكاملة (19 خطوة مترابطة - القسم 32)</span>
            </button>
          </div>
        </div>

        <!-- Attention Required Section -->
        <div class="surface-card bg-white rounded-2xl border-2 border-amber-300 p-5 shadow-xs">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <span class="w-8 h-8 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold">⚠️</span>
              <div>
                <h2 class="text-base font-extrabold text-navy">قرارات وتنبيهات تحتاج تدخل الإدارة (Attention Required)</h2>
                <p class="text-xs text-mutedtxt">خصومات استثنائية، فواتير متأخرة، محادثات تنتظر مسؤولاً، ومراجعة دمج هويات</p>
              </div>
            </div>
            <button data-nav="approvals" class="px-3 py-1.5 rounded-xl bg-navy text-white text-xs font-bold hover:bg-navy-light">فتح مركز الموافقات (${pendingApprovals.length})</button>
          </div>
          <div class="grid md:grid-cols-3 gap-3">
            ${pendingApprovals.map(ap => `
              <div class="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200 flex flex-col justify-between gap-2">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-extrabold text-amber-900">${esc(ap.request_type)}</span>
                    ${statusBadge(ap.status)}
                  </div>
                  <div class="text-xs font-bold text-slate-800 mt-1">العميل: ${esc(ap.client_name)} — ${esc(ap.amount_display)}</div>
                  <div class="text-[11px] text-slate-600 mt-0.5">${esc(ap.reason)}</div>
                </div>
                <div class="flex items-center gap-2 pt-2 border-t border-amber-200/60">
                  <button data-action="quick-approve" data-id="${esc(ap.id)}" class="px-3 py-1 rounded-lg bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700">اعتماد فوري</button>
                  <button data-nav="approvals" class="px-3 py-1 rounded-lg bg-white border border-slate-300 text-xs font-bold">مراجعة</button>
                </div>
              </div>
            `).join('')}
            ${overdueInvs.map(inv => `
              <div class="p-3.5 rounded-xl bg-red-50/70 border border-red-200 flex flex-col justify-between gap-2">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-extrabold text-red-900">فاتورة متأخرة: ${esc(inv.invoice_number)}</span>
                    ${statusBadge(inv.status)}
                  </div>
                  <div class="text-xs font-bold text-slate-800 mt-1">${esc(getContactName(inv.contact_id))}</div>
                  <div class="text-[11px] text-slate-600 mt-0.5">المتبقي: ${fmtMoney(inv.remaining_cents, inv.currency)} • الاستحقاق: ${esc(inv.due_date)}</div>
                </div>
                <div class="flex items-center gap-2 pt-2 border-t border-red-200/60">
                  <button data-nav="invoices" class="px-3 py-1 rounded-lg bg-red-600 text-white text-xs font-bold">متابعة التحصيل</button>
                </div>
              </div>
            `).join('')}
            ${humanWaitConvs.map(cv => `
              <div class="p-3.5 rounded-xl bg-blue-50/70 border border-blue-200 flex flex-col justify-between gap-2">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-extrabold text-blue-900">محادثة تنتظر موظفاً (${esc(cv.channel_name)})</span>
                    ${statusBadge(cv.status)}
                  </div>
                  <div class="text-xs font-bold text-slate-800 mt-1">${esc(getContactName(cv.contact_id))}</div>
                  <div class="text-[11px] text-slate-600 mt-0.5 truncate">${esc(cv.last_message_text)}</div>
                </div>
                <div class="flex items-center gap-2 pt-2 border-t border-blue-200/60">
                  <button data-action="open-conv-direct" data-id="${esc(cv.id)}" class="px-3 py-1 rounded-lg bg-navy text-white text-xs font-bold">الرد الآن</button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- 20 Real-time KPIs Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3.5">
          ${kpis.map(k => `
            <div data-nav="${esc(k.nav)}" class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs hover:border-teal cursor-pointer transition flex flex-col justify-between">
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-bold text-mutedtxt">${esc(k.label)}</span>
                <span class="w-8 h-8 rounded-xl bg-teal/10 text-teal flex items-center justify-center text-base">${k.icon}</span>
              </div>
              <div class="text-xl font-black text-navy my-2">${k.val}</div>
              <div class="text-[11px] text-emerald-700 font-semibold">${esc(k.sub)}</div>
            </div>
          `).join('')}
        </div>

        <!-- 8 Analytical Charts Grid -->
        <div class="grid md:grid-cols-2 xl:grid-cols-4 gap-4">
          <!-- Chart 1: Sales Performance -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">1. أداء المبيعات والعروض (Sales Performance)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">قيمة العروض حسب الحالة</p>
            <div class="space-y-2.5">
              ${['مقبول','بانتظار الاعتماد','مرسل','مسودة'].map(st => {
                const sumC = db.quotes.filter(q => q.status === st).reduce((a,x)=>a+(Number(x.total_cents)||0),0);
                const totAll = Math.max(1, db.quotes.reduce((a,x)=>a+(Number(x.total_cents)||0),0));
                const pct = Math.round((sumC / totAll) * 100);
                return `<div>
                  <div class="flex justify-between text-xs font-bold mb-1"><span>${esc(st)}</span><span>${fmtMoney(sumC)} (${pct}%)</span></div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-teal rounded-full" style="width:${Math.max(6,pct)}%"></div></div>
                </div>`;
              }).join('')}
            </div>
          </div>

          <!-- Chart 2: Revenue by Month -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">2. الإيرادات الشهرية (Revenue by Month)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">تطور التحصيلات والتعاقدات (DEMO)</p>
            <div class="h-36 flex items-end justify-between gap-2 pt-4 px-2 border-b border-slate-200">
              ${[
                {m:'أغسطس', v:35}, {m:'سبتمبر', v:52}, {m:'أكتوبر', v:68},
                {m:'نوفمبر (الحالي)', v:Math.min(100, Math.round(collectedAmount/5000))}
              ].map(bar => `
                <div class="flex-1 flex flex-col items-center gap-1">
                  <span class="text-[10px] font-bold ltr-num">${bar.v}%</span>
                  <div class="w-full bg-gradient-to-t from-navy to-teal rounded-t-lg" style="height:${Math.max(15, bar.v)}px"></div>
                  <span class="text-[10px] text-mutedtxt truncate">${bar.m}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Chart 3: Leads Conversion Funnel -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">3. قمع تحويل الفرص (Leads Funnel)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">توزيع الفرص عبر المراحل</p>
            <div class="space-y-2">
              ${['عميل محتمل جديد','تم جمع المتطلبات','تم إرسال العرض','تفاوض','مكتسب'].map(stg => {
                const cnt = db.leads.filter(l => l.stage === stg).length;
                const pct = Math.round((cnt / Math.max(1, db.leads.length)) * 100);
                return `<div>
                  <div class="flex justify-between text-xs font-semibold"><span>${esc(stg)}</span><span class="ltr-num font-bold">${cnt} (${pct}%)</span></div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden mt-0.5"><div class="h-full bg-navy-light rounded-full" style="width:${Math.max(8,pct)}%"></div></div>
                </div>`;
              }).join('')}
            </div>
          </div>

          <!-- Chart 4: Projects by Status -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">4. المشروعات حسب الحالة (Projects by Status)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">متابعة التنفيذ والجودة</p>
            <div class="space-y-2.5">
              ${['قيد التنفيذ','مراجعة داخلية','مكتمل','التخطيط'].map(st => {
                const cnt = db.projects.filter(p => p.current_stage === st).length;
                const pct = Math.round((cnt / Math.max(1, db.projects.length)) * 100);
                return `<div>
                  <div class="flex justify-between text-xs font-bold"><span>${esc(st)}</span><span class="ltr-num">${cnt} مشروع</span></div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden mt-1"><div class="h-full bg-emerald-600 rounded-full" style="width:${Math.max(8,pct)}%"></div></div>
                </div>`;
              }).join('')}
            </div>
          </div>

          <!-- Chart 5: Customer Acquisition Channels -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">5. قنوات اكتساب الباحثين (Acquisition Channels)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">توزيع العملاء حسب المنصة</p>
            <div class="space-y-2">
              ${['WhatsApp','Instagram','Website Live Chat','Email','Telegram'].map(ch => {
                const cnt = db.contacts.filter(c => c.source === ch).length;
                const pct = Math.round((cnt / Math.max(1, db.contacts.length)) * 100);
                return `<div class="flex items-center justify-between text-xs py-1 border-b border-slate-100">
                  <span class="font-bold">${esc(ch)}</span>
                  <span class="px-2 py-0.5 rounded bg-teal/10 text-teal font-bold ltr-num">${cnt} (${pct}%)</span>
                </div>`;
              }).join('')}
            </div>
          </div>

          <!-- Chart 6: Services Revenue Distribution -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">6. توزيع إيرادات الخدمات (Services Revenue)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">أعلى الخدمات الأكاديمية طلباً</p>
            <div class="space-y-2">
              ${db.quotes.slice(0, 4).map(q => `
                <div class="flex items-center justify-between text-xs py-1 border-b border-slate-100">
                  <span class="truncate max-w-[150px] font-semibold">${esc(q.title)}</span>
                  <span>${fmtMoney(q.total_cents, q.currency)}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Chart 7: AI vs Human Conversations -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">7. محادثات AI مقابل الموظفين (AI vs Human)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">توزيع إدارة المحادثات الجارية</p>
            <div class="flex items-center gap-4 my-4">
              <div class="flex-1 p-3 rounded-xl bg-teal/10 text-center">
                <div class="text-xs text-mutedtxt font-bold">إدارة وكيل AI</div>
                <div class="text-2xl font-black text-teal ltr-num mt-1">${aiConvsCount}</div>
              </div>
              <div class="flex-1 p-3 rounded-xl bg-navy/10 text-center">
                <div class="text-xs text-mutedtxt font-bold">إدارة موظف بشري</div>
                <div class="text-2xl font-black text-navy ltr-num mt-1">${humanConvsCount}</div>
              </div>
            </div>
            <div class="text-[11px] text-mutedtxt">إجمالي عمليات تشغيل الوكيل المسجلة: <b class="ltr-num">${db.ai_conversation_runs.length}</b></div>
          </div>

          <!-- Chart 8: Payment Collection Performance -->
          <div class="surface-card bg-white rounded-2xl p-4 border border-bordercol shadow-xs">
            <h3 class="text-sm font-extrabold text-navy mb-1">8. كفاءة التحصيل المالي (Collection Performance)</h3>
            <p class="text-[11px] text-mutedtxt mb-3">المحصل مقابل المستحق</p>
            <div class="space-y-3 mt-3">
              <div class="flex justify-between text-xs"><span>إجمالي المحصل المؤكد:</span><span class="text-emerald-700">${fmtMoney(collectedAmount)}</span></div>
              <div class="flex justify-between text-xs"><span>إجمالي المتبقي للتحصيل:</span><span class="text-amber-700">${fmtMoney(remainingReceivables)}</span></div>
              <div class="h-3 bg-slate-100 rounded-full overflow-hidden flex">
                <div class="bg-emerald-600 h-full" style="width:${Math.round((collectedAmount/Math.max(1,collectedAmount+remainingReceivables))*100)}%"></div>
                <div class="bg-amber-500 h-full flex-1"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // ============================================================================
  // SECTION 7 — VIEW 2: OMNICHANNEL UNIFIED INBOX (3-Column Architecture)
  // ============================================================================
  function renderInbox() {
    const filteredConvs = db.conversations.filter(c => {
      if (state.inboxChannelFilter !== 'الكل' && c.channel_name !== state.inboxChannelFilter) return false;
      if (state.inboxStatusFilter !== 'الكل' && c.status !== state.inboxStatusFilter) return false;
      if (state.inboxModeFilter !== 'الكل' && c.handling_mode !== state.inboxModeFilter) return false;
      if (state.searchQuery) {
        const hay = (getContactName(c.contact_id) + ' ' + c.last_message_text + ' ' + c.channel_name).toLowerCase();
        if (!hay.includes(state.searchQuery.toLowerCase())) return false;
      }
      return true;
    });

    const activeConv = db.conversations.find(c => c.id === state.selectedConvId) || filteredConvs[0] || db.conversations[0];
    const contact = activeConv ? db.contacts.find(x => x.id === activeConv.contact_id) : null;
    const convMessages = activeConv ? db.messages.filter(m => m.conversation_id === activeConv.id) : [];
    const contactQuotes = contact ? db.quotes.filter(q => q.contact_id === contact.id) : [];
    const contactContracts = contact ? db.contracts.filter(k => k.contact_id === contact.id) : [];
    const contactProjects = contact ? db.projects.filter(p => p.contact_id === contact.id) : [];
    const contactDebt = contact ? db.invoices.filter(i => i.contact_id === contact.id).reduce((a,x)=>a+(Number(x.remaining_cents)||0),0) : 0;
    const handoffHist = activeConv ? JSON.parse(activeConv.handoff_history_json || '[]') : [];

    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">صندوق الرسائل الموحد (Omnichannel Unified Inbox)</h1>
            <p class="text-xs text-mutedtxt">توحيد محادثات WhatsApp وMessenger وInstagram وTelegram والدردشة الحية والبريد مع عدم دمج الهويات غير المؤكدة تلقائياً</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <button data-action="simulate-inbound-msg" class="px-3.5 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-bold shadow">+ محاكاة رسالة باحث جديد</button>
            <button data-action="review-identity-merge" class="px-3.5 py-2 rounded-xl bg-amber-100 text-amber-900 border border-amber-300 text-xs font-bold">مراجعة دمج الهويات (${db.contact_identities.filter(i=>i.merge_review_status==='pending_review').length})</button>
          </div>
        </div>

        <!-- Filters Bar -->
        <div class="surface-card bg-white p-3 rounded-2xl border border-bordercol flex flex-wrap items-center gap-2.5 text-xs">
          <select data-filter="inbox-channel" class="px-3 py-2 rounded-xl border border-bordercol font-bold">
            <option value="الكل">كل القنوات</option>
            ${['WhatsApp Business','Facebook Messenger','Instagram Direct','Telegram Bot','Website Live Chat','Email (OAuth / SMTP)'].map(ch => `<option value="${esc(ch)}" ${state.inboxChannelFilter===ch?'selected':''}>${esc(ch)}</option>`).join('')}
          </select>
          <select data-filter="inbox-status" class="px-3 py-2 rounded-xl border border-bordercol font-bold">
            <option value="الكل">كل الحالات</option>
            ${['مفتوحة','انتظار الموظف','بانتظار العميل','بانتظار الاعتماد','مغلقة'].map(st => `<option value="${esc(st)}" ${state.inboxStatusFilter===st?'selected':''}>${esc(st)}</option>`).join('')}
          </select>
          <select data-filter="inbox-mode" class="px-3 py-2 rounded-xl border border-bordercol font-bold">
            <option value="الكل">الكل (AI + موظفين)</option>
            <option value="AI" ${state.inboxModeFilter==='AI'?'selected':''}>إدارة AI</option>
            <option value="Human" ${state.inboxModeFilter==='Human'?'selected':''}>إدارة بشرية</option>
          </select>
          <span class="text-mutedtxt mr-auto font-semibold">تنبيه: القنوات الخارجية تعرض حالة الربط الفعلية ولا تدعي اتصالاً بدون مفاتيح رسمية</span>
        </div>

        <!-- 3-Column Inbox Layout -->
        <div class="grid lg:grid-cols-12 gap-4 items-start">
          <!-- Column 1: Conversations List (3 cols) -->
          <div class="lg:col-span-3 surface-card bg-white rounded-2xl border border-bordercol overflow-hidden">
            <div class="p-3.5 bg-slate-50 border-b border-bordercol flex items-center justify-between">
              <span class="text-xs font-extrabold text-navy">المحادثات (${filteredConvs.length})</span>
              <span class="px-2 py-0.5 rounded-full bg-teal/10 text-teal text-[11px] font-bold">${db.conversations.reduce((a,c)=>a+(c.unread_count||0),0)} غير مقروءة</span>
            </div>
            <div class="divide-y divide-slate-100 max-h-[620px] overflow-y-auto custom-scroll">
              ${filteredConvs.map(cv => {
                const isSel = activeConv && cv.id === activeConv.id;
                const cName = getContactName(cv.contact_id);
                return `
                  <div data-action="select-conv" data-id="${esc(cv.id)}" class="p-3.5 cursor-pointer transition ${isSel ? 'bg-teal/10 border-r-4 border-teal' : 'hover:bg-slate-50'}">
                    <div class="flex items-center justify-between gap-2">
                      <span class="font-extrabold text-xs text-navy truncate">${esc(cName)}</span>
                      ${cv.unread_count ? `<span class="px-2 py-0.5 rounded-full bg-amber-500 text-white text-[10px] font-bold ltr-num">${cv.unread_count}</span>` : ''}
                    </div>
                    <div class="flex items-center gap-1.5 mt-1 text-[11px] text-mutedtxt">
                      <span class="font-bold text-teal">${esc(cv.channel_name)}</span>
                      <span>•</span>
                      <span>${esc(cv.handling_mode === 'AI' ? '🤖 AI' : '👤 موظف')}</span>
                    </div>
                    <p class="text-xs text-slate-600 truncate mt-1.5">${esc(cv.last_message_text || '')}</p>
                    <div class="flex items-center justify-between mt-2">
                      ${statusBadge(cv.status)}
                      <span class="text-[10px] text-slate-400 ltr-num">${esc(String(cv.last_message_at || '').slice(5,16))}</span>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Column 2: Active Chat Window (6 cols) -->
          <div class="lg:col-span-6 surface-card bg-white rounded-2xl border border-bordercol flex flex-col overflow-hidden">
            ${activeConv && contact ? `
              <div class="p-4 bg-slate-50 border-b border-bordercol flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-navy text-white flex items-center justify-center font-black text-sm">${esc(contact.full_name.slice(0,2))}</div>
                  <div>
                    <div class="font-extrabold text-sm text-navy">${esc(contact.full_name)}</div>
                    <div class="text-[11px] text-mutedtxt">${esc(activeConv.channel_name)} • المسؤول: ${esc(getUserName(activeConv.assigned_to))}</div>
                  </div>
                </div>
                <div class="flex flex-wrap items-center gap-1.5">
                  <button data-action="toggle-conv-ai" data-id="${esc(activeConv.id)}" class="px-2.5 py-1.5 rounded-lg text-xs font-bold border ${activeConv.handling_mode==='AI'?'bg-teal text-white border-teal':'bg-white text-slate-700 border-slate-300'}">
                    ${activeConv.handling_mode === 'AI' ? '🤖 AI مفعّل (إيقاف)' : '🤖 تفعيل AI'}
                  </button>
                  <button data-action="handoff-conv-modal" data-id="${esc(activeConv.id)}" class="px-2.5 py-1.5 rounded-lg bg-white border border-slate-300 text-xs font-bold hover:bg-slate-100">تحويل لموظف</button>
                  <button data-action="create-quote-from-conv" data-id="${esc(contact.id)}" class="px-2.5 py-1.5 rounded-lg bg-navy text-white text-xs font-bold">+ عرض سعر</button>
                </div>
              </div>

              <!-- Messages Stream -->
              <div class="p-4 space-y-3 min-h-[360px] max-h-[420px] overflow-y-auto bg-slate-50/50 custom-scroll">
                ${convMessages.map(m => {
                  const isCust = m.sender_type === 'customer';
                  const isNote = m.sender_type === 'internal_note';
                  const isAi = m.sender_type === 'ai';
                  let boxCls = 'bg-white border-slate-200 text-slate-800 mr-auto';
                  if (!isCust) boxCls = 'bg-teal/10 border-teal/30 text-navy ml-auto';
                  if (isAi) boxCls = 'bg-indigo-50 border-indigo-200 text-indigo-950 ml-auto';
                  if (isNote) boxCls = 'bg-amber-50 border-amber-300 text-amber-900 mx-auto w-full';
                  return `
                    <div class="max-w-[85%] ${isNote ? 'max-w-full' : ''} p-3.5 rounded-2xl border ${boxCls} shadow-2xs">
                      <div class="flex items-center justify-between gap-3 text-[11px] font-bold opacity-75 mb-1">
                        <span>${isNote ? '🔒 ملاحظة فريق داخلية — ' : ''}${esc(m.sender_name)}</span>
                        <span class="ltr-num">${esc(String(m.created_at).slice(0,16))}</span>
                      </div>
                      <div class="text-xs leading-relaxed whitespace-pre-wrap">${esc(m.body)}</div>
                    </div>
                  `;
                }).join('')}
              </div>

              <!-- Saved Replies & Compose Box -->
              <div class="p-3.5 bg-white border-t border-bordercol space-y-2.5">
                <div class="flex flex-wrap items-center gap-1.5 text-[11px]">
                  <span class="font-bold text-mutedtxt">ردود جاهزة:</span>
                  <button type="button" data-action="insert-saved-reply" data-text="أهلاً بحضرتك في المتحدة للخدمات التعليمية (UES). يسعدنا دعمك أكاديمياً؛ يرجى إرسال ملف خطة البحث والموعد المطلوب لتقدير عرض السعر." class="px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 font-semibold">ترحيب وطلب الملف</button>
                  <button type="button" data-action="insert-saved-reply" data-text="نظام الدفعات المعتمد لدينا هو: 30% عند التعاقد، 30% مرحلة أولى، 30% مرحلة ثانية، و10% عند التسليم النهائي." class="px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 font-semibold">شرح نظام الدفعات</button>
                  <button type="button" data-action="ai-draft-inbox" data-id="${esc(activeConv.id)}" class="px-2.5 py-1 rounded bg-indigo-100 text-indigo-800 font-bold mr-auto">🤖 توليد رد ذكي (AI Assist)</button>
                </div>
                <form id="inbox-send-form" data-conv="${esc(activeConv.id)}" class="space-y-2">
                  <textarea id="inbox-message-input" rows="2" placeholder="اكتب رسالتك للباحث أو سجل ملاحظة داخلية للفريق..." class="w-full p-3 rounded-xl border border-slate-300 text-xs"></textarea>
                  <div class="flex flex-wrap items-center justify-between gap-2">
                    <div class="flex items-center gap-2 text-xs">
                      <label class="inline-flex items-center gap-1 cursor-pointer font-bold">
                        <input type="radio" name="reply_mode" value="staff" checked class="w-3.5 h-3.5" />
                        <span>رد على الباحث</span>
                      </label>
                      <label class="inline-flex items-center gap-1 cursor-pointer font-bold text-amber-800">
                        <input type="radio" name="reply_mode" value="internal_note" class="w-3.5 h-3.5" />
                        <span>🔒 ملاحظة داخلية</span>
                      </label>
                    </div>
                    <div class="flex items-center gap-2">
                      <button type="button" data-action="send-quote-in-chat" data-id="${esc(activeConv.id)}" class="px-3 py-1.5 rounded-xl border border-slate-300 text-xs font-bold hover:bg-slate-50">📄 إرفاق عرض سعر</button>
                      <button type="submit" class="px-4 py-1.5 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">إرسال وتوثيق</button>
                    </div>
                  </div>
                </form>
              </div>
            ` : `<div class="p-8 text-center text-mutedtxt text-sm">اختر محادثة من القائمة</div>`}
          </div>

          <!-- Column 3: Customer 360 Profile (3 cols) -->
          <div class="lg:col-span-3 surface-card bg-white rounded-2xl border border-bordercol p-4 space-y-3">
            ${contact ? `
              <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                <div>
                  <h3 class="font-extrabold text-sm text-navy">${esc(contact.full_name)}</h3>
                  <p class="text-xs text-mutedtxt">${esc(contact.academic_degree)} • ${esc(contact.country)}</p>
                </div>
                ${statusBadge(contact.priority)}
              </div>
              <div class="space-y-1.5 text-xs">
                <div class="flex justify-between"><span class="text-mutedtxt">الهاتف:</span><span class="ltr-num font-bold">${esc(contact.phone)}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">البريد:</span><span class="ltr-num font-semibold truncate max-w-[160px]">${esc(contact.email)}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">الجامعة:</span><span class="font-bold">${esc(contact.university || '—')}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">التخصص:</span><span class="font-bold">${esc(contact.research_field || '—')}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">العروض السابقة:</span><span class="font-bold ltr-num">${contactQuotes.length}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">العقود:</span><span class="font-bold ltr-num">${contactContracts.length}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">المشروعات:</span><span class="font-bold ltr-num">${contactProjects.length}</span></div>
                <div class="flex justify-between"><span class="text-mutedtxt">المديونية المتبقية:</span><span class="text-red-600">${fmtMoney(contactDebt)}</span></div>
              </div>
              <div class="pt-2 border-t border-slate-100">
                <div class="text-xs font-extrabold text-navy mb-1">سجل انتقال المحادثة (AI ↔ موظف):</div>
                ${handoffHist.length ? handoffHist.map(h => `
                  <div class="text-[11px] p-2 rounded-lg bg-slate-50 border border-slate-200 mb-1">
                    <b>${esc(h.from)} ← ${esc(h.to)}</b>: ${esc(h.reason)} <span class="ltr-num text-slate-400">(${esc(h.at)})</span>
                  </div>
                `).join('') : '<div class="text-[11px] text-mutedtxt">لا توجد تحويلات سابقة</div>'}
              </div>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  }

  // ============================================================================
  // SECTION 8 — VIEW 3: CONTACTS MANAGEMENT / CRM
  // ============================================================================
  function renderContacts() {
    const list = db.contacts.filter(c => {
      if (c.is_archived) return false;
      if (state.contactDegreeFilter !== 'الكل' && c.academic_degree !== state.contactDegreeFilter) return false;
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        if (!(c.full_name + c.phone + c.email + c.university + c.country + c.research_field).toLowerCase().includes(q)) return false;
      }
      return true;
    });

    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة العملاء والباحثين (Contact Management / CRM)</h1>
            <p class="text-xs text-mutedtxt">ملفات الباحثين الأكاديمية، منع التكرار، مراجعة دمج الهويات، وقيمة العميل الدائمة (Lifetime Value)</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-action="export-csv" data-entity="contacts" class="px-3.5 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold hover:bg-slate-50">📥 تصدير CSV</button>
            <button data-action="open-contact-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إضافة باحث / عميل جديد</button>
          </div>
        </div>

        <div class="surface-card bg-white p-3 rounded-2xl border border-bordercol flex flex-wrap items-center gap-3 text-xs">
          <select data-filter="contact-degree" class="px-3 py-2 rounded-xl border border-bordercol font-bold">
            <option value="الكل">كل الدرجات العلمية</option>
            ${['دكتوراه','ماجستير','بكالوريوس','باحث مستقل'].map(d => `<option value="${esc(d)}" ${state.contactDegreeFilter===d?'selected':''}>${esc(d)}</option>`).join('')}
          </select>
          <span class="font-bold text-teal">إجمالي السجلات المعروضة: ${list.length}</span>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">المعرف</th>
                  <th class="p-3.5">الاسم الكامل والجامعة</th>
                  <th class="p-3.5">الهاتف والبريد</th>
                  <th class="p-3.5">الدولة</th>
                  <th class="p-3.5">الدرجة والتخصص</th>
                  <th class="p-3.5">القناة</th>
                  <th class="p-3.5">قيمة التعاملات LTV</th>
                  <th class="p-3.5">المسؤول</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${list.map(c => `
                  <tr class="hover:bg-slate-50/80">
                    <td class="p-3.5 font-bold ltr-num text-navy">${esc(c.id)}</td>
                    <td class="p-3.5">
                      <div class="font-extrabold text-navy">${esc(c.full_name)}</div>
                      <div class="text-[11px] text-mutedtxt">${esc(c.university || '—')} • ${esc(c.faculty || '')}</div>
                    </td>
                    <td class="p-3.5">
                      <div class="ltr-num font-semibold">${esc(c.phone)}</div>
                      <div class="text-[11px] text-mutedtxt ltr-num">${esc(c.email)}</div>
                    </td>
                    <td class="p-3.5 font-semibold">${esc(c.country)} (${esc(c.city || '')})</td>
                    <td class="p-3.5">
                      <span class="font-bold text-teal">${esc(c.academic_degree)}</span>
                      <div class="text-[11px] text-mutedtxt truncate max-w-[180px]">${esc(c.research_field)}</div>
                    </td>
                    <td class="p-3.5">${statusBadge(c.source)}</td>
                    <td class="p-3.5">${fmtMoney(c.lifetime_value_cents)}</td>
                    <td class="p-3.5 font-semibold">${esc(getUserName(c.assigned_sales_id))}</td>
                    <td class="p-3.5">
                      <div class="flex items-center gap-1.5">
                        <button data-action="view-contact-360" data-id="${esc(c.id)}" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 font-bold">ملف 360°</button>
                        <button data-action="open-contact-modal" data-id="${esc(c.id)}" class="px-2.5 py-1 rounded-lg bg-teal/10 text-teal font-bold">تعديل</button>
                      </div>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // ============================================================================
  // SECTION 9 — VIEW 4 & 5: LEADS MANAGEMENT & SALES PIPELINE KANBAN
  // ============================================================================
  const PIPELINE_STAGES = [
    'عميل محتمل جديد', 'تم التواصل', 'مؤهل', 'تم جمع المتطلبات',
    'تم إعداد العرض', 'تم إرسال العرض', 'تفاوض', 'مكتسب', 'مفقود'
  ];

  function renderLeadsTable() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة العملاء المحتملين وتقييم الفرص (Lead Management & Scoring)</h1>
            <p class="text-xs text-mutedtxt">تأهيل الباحثين وتقييم احتمالية التعاقد (Lead Scoring) استناداً إلى معايير موضوعية</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-nav="pipeline" class="px-3.5 py-2 rounded-xl bg-navy text-white text-xs font-bold">🗂️ فتح لوحة Kanban</button>
            <button data-action="open-lead-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إضافة فرصة بيعية</button>
          </div>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">المعرف</th>
                  <th class="p-3.5">عنوان الفرصة والخدمة</th>
                  <th class="p-3.5">الباحث</th>
                  <th class="p-3.5">المرحلة</th>
                  <th class="p-3.5">تقييم الفرصة (Score)</th>
                  <th class="p-3.5">القيمة التقديرية</th>
                  <th class="p-3.5">الموعد المستهدف</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.leads.map(l => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 font-bold ltr-num">${esc(l.id)}</td>
                    <td class="p-3.5">
                      <div class="font-extrabold text-navy">${esc(l.title)}</div>
                      <div class="text-[11px] text-mutedtxt">${esc(getServiceName(l.service_id))}</div>
                    </td>
                    <td class="p-3.5 font-bold">${esc(getContactName(l.contact_id))}</td>
                    <td class="p-3.5">${statusBadge(l.stage)}</td>
                    <td class="p-3.5"><span class="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 font-extrabold ltr-num">${l.lead_score}/100</span></td>
                    <td class="p-3.5">${fmtMoney(l.estimated_value_cents, l.currency)}</td>
                    <td class="p-3.5 ltr-num">${esc(l.target_delivery_date || '—')}</td>
                    <td class="p-3.5">
                      <div class="flex items-center gap-1.5">
                        <button data-action="advance-lead-stage" data-id="${esc(l.id)}" class="px-2.5 py-1 rounded-lg bg-teal/10 text-teal font-bold">نقل للمرحلة التالية</button>
                        <button data-action="quote-from-lead" data-id="${esc(l.id)}" class="px-2.5 py-1 rounded-lg bg-navy text-white font-bold">+ عرض سعر</button>
                      </div>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  function renderPipelineKanban() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">مسار المبيعات التفاعلي (Sales Pipeline Kanban — 9 Stages)</h1>
            <p class="text-xs text-mutedtxt">انقل الفرصة بين المراحل التسع أو أنشئ عرض سعر مباشرة من بطاقة الفرصة</p>
          </div>
          <button data-action="open-lead-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ فرصة جديدة</button>
        </div>

        <div class="flex gap-3.5 overflow-x-auto pb-4 custom-scroll">
          ${PIPELINE_STAGES.map(stg => {
            const cards = db.leads.filter(l => l.stage === stg);
            return `
              <div class="min-w-[260px] w-[260px] bg-slate-100/90 rounded-2xl p-3 border border-slate-200 flex flex-col gap-2.5">
                <div class="flex items-center justify-between px-1">
                  <span class="font-extrabold text-xs text-navy">${esc(stg)}</span>
                  <span class="px-2 py-0.5 rounded-full bg-white text-navy text-[11px] font-bold shadow-2xs ltr-num">${cards.length}</span>
                </div>
                <div class="space-y-2.5 min-h-[220px]">
                  ${cards.map(l => `
                    <div class="surface-card bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
                      <div class="flex items-center justify-between">
                        ${statusBadge(l.priority)}
                        <span class="text-[11px] font-bold text-emerald-700 ltr-num">Score: ${l.lead_score}%</span>
                      </div>
                      <div class="font-extrabold text-xs text-navy">${esc(l.title)}</div>
                      <div class="text-[11px] text-mutedtxt">👤 ${esc(getContactName(l.contact_id))}</div>
                      <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
                        <span>${fmtMoney(l.estimated_value_cents, l.currency)}</span>
                        <div class="flex gap-1">
                          <button data-action="advance-lead-stage" data-id="${esc(l.id)}" class="px-2 py-1 rounded bg-teal/10 text-teal text-[11px] font-bold" title="تقدم للمرحلة التالية">← تقدم</button>
                          <button data-action="quote-from-lead" data-id="${esc(l.id)}" class="px-2 py-1 rounded bg-navy text-white text-[11px] font-bold">عرض</button>
                        </div>
                      </div>
                    </div>
                  `).join('') || '<div class="text-center text-xs text-slate-400 py-8">لا توجد فرص في هذه المرحلة</div>'}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  // ============================================================================
  // SECTION 10 — VIEW 6: ACADEMIC SERVICE CATALOG
  // ============================================================================
  function renderCatalog() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">كتالوج الخدمات الأكاديمية والمهنية (Academic Service Catalog)</h1>
            <p class="text-xs text-mutedtxt">6 تصنيفات تخصصية شاملة — جميع الأسعار المعروضة مصنفة بوضوح <span class="font-bold text-amber-700">DEMO</span> لأغراض التجربة</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-nav="pricing" class="px-3.5 py-2 rounded-xl bg-navy text-white text-xs font-bold">🧮 فتح حاسبة التسعير الذكي</button>
            <button data-action="open-service-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إضافة خدمة للكتالوج</button>
          </div>
        </div>

        <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          ${db.services.map(s => `
            <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 shadow-xs flex flex-col justify-between gap-3">
              <div class="space-y-2">
                <div class="flex items-center justify-between gap-2">
                  <span class="px-2.5 py-0.5 rounded-full bg-teal/10 text-teal text-xs font-bold">${esc(s.category_name_ar)}</span>
                  <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-900 text-[10px] font-extrabold ltr-num">${esc(s.service_code)} • DEMO</span>
                </div>
                <h3 class="text-base font-extrabold text-navy">${esc(s.name_ar)}</h3>
                <div class="text-[11px] font-semibold text-slate-500 ltr-num">${esc(s.name_en)}</div>
                <p class="text-xs text-slate-600 leading-relaxed">${esc(s.description)}</p>
                <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-[11px] space-y-1">
                  <div><b>المخرجات:</b> ${esc(s.deliverables)}</div>
                  <div><b>المستندات المطلوبة:</b> ${esc(s.required_documents)}</div>
                  <div><b>القسم المختص:</b> ${esc(s.assigned_department)} • <b>طريقة التسعير:</b> <span class="ltr-num">${esc(s.pricing_method)}</span></div>
                </div>
              </div>
              <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                <div>
                  <div class="text-[10px] text-mutedtxt font-bold">السعر الأساسي (DEMO)</div>
                  <div class="text-lg font-black text-navy">${fmtMoney(s.base_price_cents, s.currency)}</div>
                </div>
                <div class="text-left">
                  <div class="text-[10px] text-mutedtxt font-bold">المدة / الساعات</div>
                  <div class="text-xs font-bold">${s.min_duration_days} أيام (${s.estimated_hours} ساعة)</div>
                </div>
                <button data-action="price-this-service" data-id="${esc(s.id)}" class="px-3 py-1.5 rounded-xl bg-teal text-white text-xs font-bold hover:bg-teal-hover">تسعير الآن</button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // ============================================================================
  // SECTION 11 — VIEW 7: SMART PRICING ENGINE
  // ============================================================================
  function renderPricingEngine() {
    const calc = computePricing(
      state.calcServiceId,
      state.calcQty,
      state.calcComplexity,
      state.calcUrgency,
      state.calcAcademic,
      state.calcDiscountPct,
      state.calcTaxPct,
      state.calcCurrency
    );

    return `
      <div class="space-y-5">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">محرك التسعير الذكي متعدد العملات (Smart Pricing Engine)</h1>
            <p class="text-xs text-mutedtxt">المعادلة الخادمية الدقيقة: السعر الأساسي × الكمية × معامل التعقيد × معامل الاستعجال × معامل الدرجة − الخصم + الضريبة</p>
          </div>
          <span class="px-3 py-1.5 rounded-xl bg-amber-100 text-amber-900 text-xs font-bold">سقف الخصم التلقائي: ${calc.maxLimit}% (ما زاد يتطلب موافقة المدير)</span>
        </div>

        <div class="grid lg:grid-cols-12 gap-5 items-start">
          <div class="lg:col-span-7 surface-card bg-white rounded-2xl border border-bordercol p-6 space-y-4 shadow-xs">
            <h3 class="text-base font-extrabold text-navy border-b border-slate-100 pb-2">مدخلات التسعير وتكوين العرض</h3>
            <div class="grid sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label class="block font-bold mb-1">اختر الباحث / العميل</label>
                <select id="calc-contact" class="w-full p-2.5 rounded-xl border border-slate-300 font-semibold">
                  ${db.contacts.map(c => `<option value="${esc(c.id)}" ${state.calcContactId===c.id?'selected':''}>${esc(c.full_name)} (${esc(c.academic_degree)})</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block font-bold mb-1">اختر الخدمة الأكاديمية</label>
                <select id="calc-service" class="w-full p-2.5 rounded-xl border border-slate-300 font-semibold">
                  ${db.services.map(s => `<option value="${esc(s.id)}" ${state.calcServiceId===s.id?'selected':''}>${esc(s.name_ar)} (${fmtMoneyPlain(s.base_price_cents, s.currency)})</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block font-bold mb-1">الكمية (وحدة / صفحة / تحليل / ساعة)</label>
                <input type="number" id="calc-qty" min="1" max="500" value="${state.calcQty}" class="w-full p-2.5 rounded-xl border border-slate-300 ltr-num font-bold" />
              </div>
              <div>
                <label class="block font-bold mb-1">مستوى التعقيد (Complexity Multiplier)</label>
                <select id="calc-complexity" class="w-full p-2.5 rounded-xl border border-slate-300 font-semibold">
                  <option value="قياسي" ${state.calcComplexity==='قياسي'?'selected':''}>قياسي (×1.00)</option>
                  <option value="متقدم" ${state.calcComplexity==='متقدم'?'selected':''}>متقدم — نماذج مركبة (×1.25)</option>
                  <option value="عالي التخصص" ${state.calcComplexity==='عالي التخصص'?'selected':''}>عالي التخصص — طبي/هندسي (×1.50)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold mb-1">مستوى الاستعجال (Urgency Multiplier)</label>
                <select id="calc-urgency" class="w-full p-2.5 rounded-xl border border-slate-300 font-semibold">
                  <option value="عادي" ${state.calcUrgency==='عادي'?'selected':''}>عادي (×1.00)</option>
                  <option value="سريع" ${state.calcUrgency==='سريع'?'selected':''}>سريع — أولوية قصوى (×1.20)</option>
                  <option value="عاجل جداً" ${state.calcUrgency==='عاجل جداً'?'selected':''}>عاجل جداً — طوارئ أكاديمية (×1.40)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold mb-1">المرحلة العلمية (Academic Level Multiplier)</label>
                <select id="calc-academic" class="w-full p-2.5 rounded-xl border border-slate-300 font-semibold">
                  <option value="بكالوريوس" ${state.calcAcademic==='بكالوريوس'?'selected':''}>بكالوريوس (×0.90)</option>
                  <option value="ماجستير" ${state.calcAcademic==='ماجستير'?'selected':''}>ماجستير (×1.00)</option>
                  <option value="دكتوراه" ${state.calcAcademic==='دكتوراه'?'selected':''}>دكتوراه / نشر Q1 (×1.20)</option>
                </select>
              </div>
              <div>
                <label class="block font-bold mb-1">نسبة الخصم المطلوبة (%)</label>
                <input type="number" id="calc-discount" min="0" max="60" step="0.5" value="${state.calcDiscountPct}" class="w-full p-2.5 rounded-xl border border-slate-300 ltr-num font-bold" />
              </div>
              <div>
                <label class="block font-bold mb-1">العملة (EGP, SAR, USD, IQD, AED)</label>
                <select id="calc-currency" class="w-full p-2.5 rounded-xl border border-slate-300 font-bold ltr-num">
                  ${['EGP','SAR','USD','AED','IQD'].map(curr => `<option value="${curr}" ${state.calcCurrency===curr?'selected':''}>${curr}</option>`).join('')}
                </select>
              </div>
            </div>
          </div>

          <!-- Output Breakdown Card -->
          <div class="lg:col-span-5 surface-card bg-navy text-white rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-white/15 pb-3">
              <div>
                <div class="text-xs text-teal-soft font-bold">نتيجة الحساب الدقيق (DEMO Pricing)</div>
                <h3 class="text-lg font-black mt-0.5">${esc(calc.svc.name_ar)}</h3>
              </div>
              <span class="px-2.5 py-1 rounded-lg bg-white/10 text-xs font-bold ltr-num">${esc(state.calcCurrency)}</span>
            </div>

            <div class="space-y-2 text-xs">
              <div class="flex justify-between"><span>السعر الأساسي × الكمية (${calc.quantity}):</span><span>${fmtMoney(calc.baseCents * calc.quantity, 'EGP')}</span></div>
              <div class="flex justify-between"><span>معاملات (التعقيد ×${calc.compM} • الاستعجال ×${calc.urgM} • الدرجة ×${calc.acadM}):</span><span>${fmtMoney(calc.grossCents, 'EGP')}</span></div>
              <div class="flex justify-between text-amber-300"><span>الخصم (${calc.dPct}%):</span><span>- ${fmtMoney(calc.discCents, 'EGP')}</span></div>
              <div class="flex justify-between"><span>الضريبة المطبقة (${calc.tPct}%):</span><span>+ ${fmtMoney(calc.taxCents, 'EGP')}</span></div>
              <div class="flex justify-between pt-2 border-t border-white/15 text-sm font-bold">
                <span>الإجمالي النهائي بالعملة المختارة:</span>
                <span class="text-2xl font-black text-teal-soft">${fmtMoney(calc.convertedCents, state.calcCurrency)}</span>
              </div>
              <div class="text-[11px] text-slate-300">سعر الصرف الاسترشادي المسجل بتاريخ 2026-11-10: <span class="ltr-num">1 ${state.calcCurrency} = ${calc.fxRate} EGP</span></div>
            </div>

            <div class="p-3.5 rounded-xl bg-white/10 space-y-1 text-xs">
              <div class="flex justify-between"><span>التكلفة التشغيلية التقديرية:</span><span>${fmtMoney(calc.estCostCents, state.calcCurrency)}</span></div>
              <div class="flex justify-between text-emerald-300 font-bold"><span>هامش الربح التقديري:</span><span>${fmtMoney(calc.estMarginCents, state.calcCurrency)}</span></div>
            </div>

            ${calc.requiresApproval ? `
              <div class="p-3 rounded-xl bg-amber-500/20 border border-amber-400 text-amber-200 text-xs font-bold">
                ⚠️ تنبيه حوكمة: الخصم المدخل (${calc.dPct}%) يتجاوز السقف المسموح (${calc.maxLimit}%). سيتم حفظ العرض بحالة «بانتظار الاعتماد» وإرساله إلى قسم الموافقات الإدارية تلقائياً.
              </div>
            ` : `
              <div class="p-3 rounded-xl bg-emerald-500/20 border border-emerald-400 text-emerald-200 text-xs font-bold">
                ✅ الخصم ضمن السقف المسموح (${calc.maxLimit}%). يمكن إصدار العرض مباشرة.
              </div>
            `}

            <button data-action="create-quote-from-calculator" class="w-full py-3 rounded-xl bg-teal hover:bg-teal-hover text-white font-black text-sm shadow-lg transition">
              📄 إنشاء وحفظ عرض السعر الآن
            </button>
          </div>
        </div>
      </div>
    `;
  }


  // ============================================================================
  // Views 8 to 16 (Quotes, Contracts, Projects ERP [5 views], Tasks, Timeline, Team, Invoices, Payments, Reports)
  // ============================================================================

  // SECTION 12 — VIEW 8: QUOTATION MANAGEMENT
  function renderQuotes() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة عروض الأسعار والاعتمادات (Quotation Management)</h1>
            <p class="text-xs text-mutedtxt">تثبيت نسخة السعر وقت القبول (Snapshot) بحيث لا تتأثر العروض المقبولة أو العقود بتغير كتالوج الأسعار لاحقاً</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-nav="pricing" class="px-3.5 py-2 rounded-xl bg-navy text-white text-xs font-bold">🧮 إنشاء عبر حاسبة التسعير</button>
            <button data-action="export-csv" data-entity="quotes" class="px-3.5 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">📥 تصدير CSV</button>
          </div>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">رقم العرض</th>
                  <th class="p-3.5">الباحث / العميل</th>
                  <th class="p-3.5">الخدمة والنطاق</th>
                  <th class="p-3.5">الخصم والضريبة</th>
                  <th class="p-3.5">الإجمالي المثبت</th>
                  <th class="p-3.5">صالح حتى</th>
                  <th class="p-3.5">الحالة</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.quotes.map(q => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 font-extrabold text-navy ltr-num">${esc(q.quote_number)}</td>
                    <td class="p-3.5 font-bold">${esc(getContactName(q.contact_id))}</td>
                    <td class="p-3.5">
                      <div class="font-extrabold text-navy">${esc(q.title)}</div>
                      <div class="text-[11px] text-mutedtxt truncate max-w-[220px]">${esc(q.description)}</div>
                    </td>
                    <td class="p-3.5 ltr-num">خصم ${q.discount_pct}% • ضريبة ${q.tax_pct}%</td>
                    <td class="p-3.5">${fmtMoney(q.total_cents, q.currency)}</td>
                    <td class="p-3.5 ltr-num">${esc(q.valid_until)}</td>
                    <td class="p-3.5">${statusBadge(q.status)}</td>
                    <td class="p-3.5">
                      <div class="flex flex-wrap items-center gap-1.5">
                        <button data-action="preview-quote-pdf" data-id="${esc(q.id)}" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 font-bold">معاينة PDF (AR/EN)</button>
                        ${q.status === 'مسودة' ? `<button data-action="quote-next-status" data-id="${esc(q.id)}" data-next="مرسل" class="px-2.5 py-1 rounded-lg bg-teal text-white font-bold">إرسال للباحث</button>` : ''}
                        ${q.status === 'بانتظار الاعتماد' ? `<button data-action="approve-quote-btn" data-id="${esc(q.id)}" class="px-2.5 py-1 rounded-lg bg-amber-600 text-white font-bold">اعتماد المدير</button>` : ''}
                        ${q.status === 'معتمد' ? `<button data-action="quote-next-status" data-id="${esc(q.id)}" data-next="مرسل" class="px-2.5 py-1 rounded-lg bg-teal text-white font-bold">إرسال العرض</button>` : ''}
                        ${q.status === 'مرسل' ? `<button data-action="quote-next-status" data-id="${esc(q.id)}" data-next="مقبول" class="px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-bold">تسجيل قبول الباحث</button>` : ''}
                        ${q.status === 'مقبول' && !db.contracts.some(k=>k.quote_id===q.id) ? `<button data-action="open-contract-from-quote" data-id="${esc(q.id)}" class="px-2.5 py-1 rounded-lg bg-navy text-white font-bold">+ إنشاء عقد</button>` : ''}
                      </div>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 13 — VIEW 9: CONTRACT MANAGEMENT
  function renderContracts() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة العقود والاتفاقيات وجدول الأقساط (Contract Management)</h1>
            <p class="text-xs text-mutedtxt">نموذج الأقساط القياسي 30% تعاقد + 30% مرحلة أولى + 30% مرحلة ثانية + 10% تسليم نهائي (بشرط إجمالي = 100%)</p>
          </div>
          <button data-action="open-new-contract-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إعداد عقد من عرض مقبول</button>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">رقم العقد</th>
                  <th class="p-3.5">الباحث</th>
                  <th class="p-3.5">عنوان العقد والمرجع</th>
                  <th class="p-3.5">القيمة التعاقدية</th>
                  <th class="p-3.5">جدول الأقساط (%)</th>
                  <th class="p-3.5">موعد التسليم</th>
                  <th class="p-3.5">حالة التوقيع / الموافقة</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.contracts.map(k => {
                  const inst = JSON.parse(k.installments_json || '[30,30,30,10]');
                  const hasProj = db.projects.some(p => p.contract_id === k.id);
                  return `
                    <tr class="hover:bg-slate-50">
                      <td class="p-3.5 font-extrabold text-navy ltr-num">${esc(k.contract_number)}</td>
                      <td class="p-3.5 font-bold">${esc(getContactName(k.contact_id))}</td>
                      <td class="p-3.5">
                        <div class="font-extrabold text-navy">${esc(k.title)}</div>
                        <div class="text-[11px] text-mutedtxt">مرجع العرض: <span class="ltr-num">${esc(k.quote_id)}</span></div>
                      </td>
                      <td class="p-3.5">${fmtMoney(k.contract_value_cents, k.currency)}</td>
                      <td class="p-3.5"><span class="px-2 py-1 rounded bg-teal/10 text-teal font-bold ltr-num">${inst.join('% / ')}%</span></td>
                      <td class="p-3.5 ltr-num font-bold">${esc(k.agreed_deadline)}</td>
                      <td class="p-3.5">${statusBadge(k.signature_status)}</td>
                      <td class="p-3.5">
                        <div class="flex flex-wrap items-center gap-1.5">
                          <button data-action="view-contract-template" data-id="${esc(k.id)}" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 font-bold">نص العقد (AR/EN)</button>
                          ${!hasProj ? `<button data-action="convert-contract-to-project" data-id="${esc(k.id)}" class="px-2.5 py-1 rounded-lg bg-navy text-white font-bold">🚀 تحويل إلى مشروع</button>` : `<span class="text-[11px] text-emerald-700 font-bold">✓ مرتبط بمشروع</span>`}
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 14 — VIEW 10: PROJECT MANAGEMENT ERP (5 Views: Table, Kanban, Calendar, Timeline, Gantt)
  function calcProjectProgress(projId) {
    const pTasks = db.tasks.filter(t => t.project_id === projId);
    if (!pTasks.length) {
      const p = db.projects.find(x => x.id === projId);
      return p ? Number(p.progress_pct) || 0 : 0;
    }
    const sumPct = pTasks.reduce((a, t) => a + (t.status === 'مكتملة' ? 100 : Number(t.progress_pct) || 0), 0);
    return Math.round(sumPct / pTasks.length);
  }

  function renderProjectsERP() {
    // Role-based filtering: Academic Specialist sees only assigned projects
    const visibleProjects = db.projects.filter(p => {
      if (state.currentRole === 'academic_specialist') {
        const teamArr = JSON.parse(p.assigned_team_json || '[]');
        return teamArr.includes(state.currentUser.id) || db.tasks.some(t => t.project_id === p.id && t.assigned_to === state.currentUser.id);
      }
      return true;
    });

    const mode = state.projectViewMode;

    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة المشروعات الأكاديمية (Project Management ERP)</h1>
            <p class="text-xs text-mutedtxt">متابعة مراحل التنفيذ، الميزانية والتكلفة الداخلية، وحساب نسب الإنجاز تلقائياً من المهام</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <div class="inline-flex rounded-xl border border-bordercol bg-white p-1 text-xs font-bold">
              ${[
                ['table','📋 جدول (Table)'],
                ['kanban','🗂️ كانبان (Kanban)'],
                ['gantt','📊 جانت (Gantt)'],
                ['timeline','⏱️ خط زمني (Timeline)'],
                ['calendar','📅 تقويم (Calendar)']
              ].map(([m, lbl]) => `
                <button data-action="set-project-view" data-mode="${m}" class="px-3 py-1.5 rounded-lg transition ${mode===m ? 'bg-navy text-white' : 'text-slate-600 hover:bg-slate-100'}">${lbl}</button>
              `).join('')}
            </div>
            <button data-action="open-project-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ مشروع جديد</button>
          </div>
        </div>

        ${mode === 'table' ? `
          <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
            <div class="overflow-x-auto">
              <table class="w-full text-right text-xs">
                <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                  <tr>
                    <th class="p-3.5">كود المشروع</th>
                    <th class="p-3.5">عنوان المشروع والباحث</th>
                    <th class="p-3.5">القسم ومدير المشروع</th>
                    <th class="p-3.5">المرحلة الحالية</th>
                    <th class="p-3.5">نسبة الإنجاز</th>
                    <th class="p-3.5">الميزانية / التكلفة</th>
                    <th class="p-3.5">موعد التسليم</th>
                    <th class="p-3.5">الإجراءات</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  ${visibleProjects.map(p => {
                    const prog = calcProjectProgress(p.id);
                    return `
                      <tr class="hover:bg-slate-50">
                        <td class="p-3.5 font-extrabold text-navy ltr-num">${esc(p.project_code)}</td>
                        <td class="p-3.5">
                          <div class="font-extrabold text-navy">${esc(p.title)}</div>
                          <div class="text-[11px] text-mutedtxt">👤 ${esc(getContactName(p.contact_id))}</div>
                        </td>
                        <td class="p-3.5">
                          <div class="font-bold">${esc(p.academic_department)}</div>
                          <div class="text-[11px] text-mutedtxt">${esc(getUserName(p.manager_id))}</div>
                        </td>
                        <td class="p-3.5">${statusBadge(p.current_stage)}</td>
                        <td class="p-3.5 w-40">
                          <div class="flex justify-between text-[11px] font-bold mb-1"><span>الإنجاز</span><span class="ltr-num">${prog}%</span></div>
                          <div class="h-2 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-teal rounded-full" style="width:${prog}%"></div></div>
                        </td>
                        <td class="p-3.5">
                          <div>${fmtMoney(p.budget_cents, p.currency)}</div>
                          <div class="text-[10px] text-mutedtxt">تكلفة: ${fmtMoney(p.internal_cost_cents, p.currency)}</div>
                        </td>
                        <td class="p-3.5 ltr-num font-bold">${esc(p.deadline)}</td>
                        <td class="p-3.5">
                          <div class="flex items-center gap-1.5">
                            <button data-action="advance-project-stage" data-id="${esc(p.id)}" class="px-2.5 py-1 rounded-lg bg-teal/10 text-teal font-bold">تحديث المرحلة</button>
                            <button data-action="open-task-modal" data-project="${esc(p.id)}" class="px-2.5 py-1 rounded-lg bg-navy text-white font-bold">+ مهمة</button>
                          </div>
                        </td>
                      </tr>
                    `;
                  }).join('')}
                </tbody>
              </table>
            </div>
          </div>
        ` : ''}

        ${mode === 'kanban' ? `
          <div class="grid md:grid-cols-4 gap-4">
            ${['التخطيط','قيد التنفيذ','مراجعة داخلية','مكتمل'].map(stg => {
              const cols = visibleProjects.filter(p => p.current_stage === stg);
              return `
                <div class="bg-slate-100 rounded-2xl p-3.5 border border-slate-200 space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="font-extrabold text-xs text-navy">${esc(stg)}</span>
                    <span class="px-2 py-0.5 rounded-full bg-white text-xs font-bold ltr-num">${cols.length}</span>
                  </div>
                  ${cols.map(p => {
                    const prog = calcProjectProgress(p.id);
                    return `
                      <div class="surface-card bg-white p-4 rounded-xl border border-slate-200 shadow-2xs space-y-2">
                        <div class="flex justify-between items-center">${statusBadge(p.priority)}<span class="text-[11px] font-bold ltr-num">${esc(p.project_code)}</span></div>
                        <div class="font-extrabold text-xs text-navy">${esc(p.title)}</div>
                        <div class="text-[11px] text-mutedtxt">👤 ${esc(getContactName(p.contact_id))}</div>
                        <div class="h-2 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-teal" style="width:${prog}%"></div></div>
                        <div class="flex justify-between text-[11px] text-mutedtxt"><span>الإنجاز: ${prog}%</span><span class="ltr-num">📅 ${esc(p.deadline)}</span></div>
                      </div>
                    `;
                  }).join('') || '<div class="text-xs text-slate-400 text-center py-6">لا توجد مشروعات</div>'}
                </div>
              `;
            }).join('')}
          </div>
        ` : ''}

        ${mode === 'gantt' || mode === 'timeline' || mode === 'calendar' ? `
          <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-4">
            <h3 class="text-sm font-extrabold text-navy">مخطط جانت والجدول الزمني للمشروعات (Gantt & Timeline View — نوفمبر 2026)</h3>
            <div class="space-y-3">
              ${visibleProjects.map(p => {
                const prog = calcProjectProgress(p.id);
                return `
                  <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                    <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
                      <span class="font-extrabold text-navy">${esc(p.project_code)} — ${esc(p.title)}</span>
                      <span class="ltr-num font-bold text-teal">${esc(p.start_date)} → ${esc(p.deadline)} (${prog}%)</span>
                    </div>
                    <div class="w-full h-5 bg-slate-200 rounded-lg overflow-hidden relative">
                      <div class="h-full bg-gradient-to-l from-teal to-navy text-white text-[10px] font-bold flex items-center justify-center" style="width:${Math.max(15, prog)}%">${prog}% مكتمل</div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }

  // SECTION 15 — VIEW 11: TASK MANAGEMENT
  function renderTasks() {
    const visibleTasks = db.tasks.filter(t => {
      if (state.currentRole === 'academic_specialist') return t.assigned_to === state.currentUser.id;
      return true;
    });

    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة المهام والمتابعة ومراجعة الجودة (Task Management)</h1>
            <p class="text-xs text-mutedtxt">توزيع المهام الأكاديمية والإحصائية، قوائم التحقق (Checklists)، الساعات الفعلية مقابل التقديرية، واعتماد الإنجاز</p>
          </div>
          <button data-action="open-task-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إضافة مهمة جديدة</button>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">كود المهمة</th>
                  <th class="p-3.5">المهمة والمشروع</th>
                  <th class="p-3.5">الأخصائي المكلف</th>
                  <th class="p-3.5">تاريخ الاستحقاق</th>
                  <th class="p-3.5">الساعات (فعلي/مقدر)</th>
                  <th class="p-3.5">الأولوية</th>
                  <th class="p-3.5">الحالة</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${visibleTasks.map(t => {
                  const proj = db.projects.find(p => p.id === t.project_id);
                  return `
                    <tr class="hover:bg-slate-50">
                      <td class="p-3.5 font-bold ltr-num text-navy">${esc(t.task_code)}</td>
                      <td class="p-3.5">
                        <div class="font-extrabold text-navy">${esc(t.title)}</div>
                        <div class="text-[11px] text-mutedtxt">🚀 ${esc(proj ? proj.title : t.project_id)}</div>
                      </td>
                      <td class="p-3.5 font-bold">${esc(getUserName(t.assigned_to))}</td>
                      <td class="p-3.5 ltr-num font-bold">${esc(t.due_date)}</td>
                      <td class="p-3.5 ltr-num">${t.actual_hours} / ${t.estimated_hours} hrs</td>
                      <td class="p-3.5">${statusBadge(t.priority)}</td>
                      <td class="p-3.5">${statusBadge(t.status)}</td>
                      <td class="p-3.5">
                        <div class="flex items-center gap-1.5">
                          ${t.status !== 'مكتملة' ? `<button data-action="complete-task" data-id="${esc(t.id)}" class="px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-bold">✓ إنجاز واعتماد</button>` : `<button data-action="reopen-task" data-id="${esc(t.id)}" class="px-2.5 py-1 rounded-lg bg-slate-100 font-bold">إعادة فتح</button>`}
                          <button data-action="remind-task" data-id="${esc(t.id)}" class="px-2.5 py-1 rounded-lg bg-amber-100 text-amber-900 font-bold">🔔 تذكير</button>
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // VIEW 12: TIMELINE & SCHEDULE
  function renderTimelineSchedule() {
    const events = [
      ...db.projects.map(p => ({ date: p.deadline, type: 'تسليم مشروع', title: p.title, owner: getUserName(p.manager_id), status: p.current_stage })),
      ...db.tasks.map(t => ({ date: t.due_date, type: 'استحقاق مهمة', title: t.title, owner: getUserName(t.assigned_to), status: t.status })),
      ...db.invoices.filter(i => i.remaining_cents > 0).map(i => ({ date: i.due_date, type: 'استحقاق فاتورة', title: `${i.invoice_number} — ${i.milestone_title}`, owner: getContactName(i.contact_id), status: i.status }))
    ].sort((a, b) => String(a.date).localeCompare(String(b.date)));

    return `
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-black text-navy">الجدول الزمني والاستحقاقات الموحدة (Master Schedule & Timeline)</h1>
            <p class="text-xs text-mutedtxt">متابعة زمنية متكاملة لمواعيد تسليم المشروعات، المهام الأكاديمية، ومواعيد استحقاق الفواتير</p>
          </div>
        </div>
        <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3">
          ${events.map(ev => `
            <div class="p-3.5 rounded-xl border border-slate-200 hover:border-teal flex flex-wrap items-center justify-between gap-3">
              <div class="flex items-center gap-3">
                <div class="px-3 py-1.5 rounded-xl bg-navy text-white text-xs font-extrabold ltr-num">${esc(ev.date)}</div>
                <div>
                  <span class="text-[11px] font-bold text-teal">${esc(ev.type)}</span>
                  <div class="text-xs font-extrabold text-navy">${esc(ev.title)}</div>
                  <div class="text-[11px] text-mutedtxt">المسؤول / الباحث: ${esc(ev.owner)}</div>
                </div>
              </div>
              ${statusBadge(ev.status)}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // SECTION 16 — VIEW 13: TEAM & EMPLOYEE MANAGEMENT
  function renderTeam() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">فريق العمل والطاقة الاستيعابية (Team & Workload Capacity Engine)</h1>
            <p class="text-xs text-mutedtxt">محرك تحديد مواعيد التسليم يعتمد على السعة الاستيعابية الحقيقية لكل أخصائي أكاديمي وإحصائي</p>
          </div>
          ${state.currentRole === "super_admin" ? `<button data-action="open-create-user-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إنشاء حساب موظف جديد (خاص بالأدمن Ahmed_99)</button>` : `<span class="px-3 py-1.5 rounded-xl bg-amber-100 text-amber-900 text-xs font-bold">🔒 إضافة حسابات الموظفين متاحة للأدمن فقط</span>`}
        </div>

        <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          ${db.profiles.map(prof => {
            const u = db.users.find(x => x.id === prof.user_id);
            const avail = db.team_availability.find(a => a.user_id === prof.user_id) || { available_hours_weekly: 40, allocated_hours_weekly: 16 };
            const activeTasksCount = db.tasks.filter(t => t.assigned_to === prof.user_id && t.status !== 'مكتملة').length;
            const loadPct = Math.min(100, Math.round((avail.allocated_hours_weekly / Math.max(1, avail.available_hours_weekly)) * 100));
            const skills = JSON.parse(prof.skills_json || '[]');
            return `
              <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3 shadow-xs">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-11 h-11 rounded-2xl bg-navy text-white flex items-center justify-center font-black text-sm">${esc(prof.avatar_initials || 'U')}</div>
                    <div>
                      <h3 class="font-extrabold text-sm text-navy">${esc(prof.full_name)}</h3>
                      <p class="text-xs text-mutedtxt">${esc(prof.job_title)}</p>
                    </div>
                  </div>
                  ${statusBadge(prof.availability_status)}
                </div>
                <div class="text-xs space-y-1 text-slate-600">
                  <div><b>القسم:</b> ${esc(prof.department)}</div>
                  <div><b>التخصص:</b> ${esc(prof.academic_specialization)}</div>
                  <div><b>الدور الوظيفي:</b> <span class="ltr-num font-bold text-teal">${esc(u ? u.role_code : '')}</span></div>
                </div>
                <div class="flex flex-wrap gap-1">
                  ${skills.map(sk => `<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-semibold">${esc(sk)}</span>`).join('')}
                </div>
                <div class="pt-2 border-t border-slate-100">
                  <div class="flex justify-between text-xs font-bold mb-1">
                    <span>السعة الأسبوعية المشغولة (${activeTasksCount} مهام نشطة)</span>
                    <span class="ltr-num">${avail.allocated_hours_weekly}/${avail.available_hours_weekly} hrs (${loadPct}%)</span>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full ${loadPct > 80 ? 'bg-amber-500' : 'bg-teal'} rounded-full" style="width:${loadPct}%"></div>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  // SECTION 17 — VIEW 14 & 15: INVOICES, PAYMENTS, INSTALLMENTS & EXPENSES
  function renderInvoices() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة الفواتير والمطالبات المالية (Invoices Management)</h1>
            <p class="text-xs text-mutedtxt">متابعة الفواتير الصادرة، المدفوعة جزئياً، المدفوعة بالكامل، والمتأخرة مع ربطها بالعقود</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-action="export-csv" data-entity="invoices" class="px-3.5 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">📥 تصدير CSV</button>
            <button data-action="open-invoice-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ إصدار فاتورة جديدة</button>
          </div>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">رقم الفاتورة</th>
                  <th class="p-3.5">الباحث</th>
                  <th class="p-3.5">البيان / القسط</th>
                  <th class="p-3.5">إجمالي الفاتورة</th>
                  <th class="p-3.5">المدفوع</th>
                  <th class="p-3.5">المتبقي</th>
                  <th class="p-3.5">الاستحقاق</th>
                  <th class="p-3.5">الحالة</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.invoices.map(i => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 font-extrabold text-navy ltr-num">${esc(i.invoice_number)}</td>
                    <td class="p-3.5 font-bold">${esc(getContactName(i.contact_id))}</td>
                    <td class="p-3.5 font-semibold">${esc(i.milestone_title)}</td>
                    <td class="p-3.5">${fmtMoney(i.amount_cents, i.currency)}</td>
                    <td class="p-3.5 text-emerald-700">${fmtMoney(i.paid_cents, i.currency)}</td>
                    <td class="p-3.5 text-red-600">${fmtMoney(i.remaining_cents, i.currency)}</td>
                    <td class="p-3.5 ltr-num font-bold">${esc(i.due_date)}</td>
                    <td class="p-3.5">${statusBadge(i.status)}</td>
                    <td class="p-3.5">
                      ${i.remaining_cents > 0 ? `<button data-action="open-payment-modal" data-invoice="${esc(i.id)}" class="px-3 py-1 rounded-lg bg-teal text-white font-bold">💳 تسجيل وتأكيد دفعة</button>` : `<span class="text-emerald-700 font-bold">✓ مسددة بالكامل</span>`}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  function renderPaymentsAndInstallments() {
    const totalCollected = db.payments.reduce((a, p) => a + (Number(p.amount_cents) || 0), 0);
    const totalExpenses = db.expenses.reduce((a, e) => a + (Number(e.amount_cents) || 0), 0);

    return `
      <div class="space-y-5">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">المدفوعات والأقساط والمصروفات التشغيلية (Payments, Installments & Expenses)</h1>
            <p class="text-xs text-mutedtxt">تأكيد الدفع يتم حصراً عبر موظف مالي مخول مع مستند إثبات أو Webhook موثوق + منع تكرار رقم المرجع (Idempotency)</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-action="open-expense-modal" class="px-3.5 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">+ تسجيل مصروف</button>
            <button data-action="open-payment-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ تسجيل دفعة مؤكدة</button>
          </div>
        </div>

        <div class="grid sm:grid-cols-3 gap-4">
          <div class="surface-card bg-white p-4 rounded-2xl border border-bordercol">
            <div class="text-xs text-mutedtxt font-bold">إجمالي المدفوعات المؤكدة</div>
            <div class="text-2xl font-black text-emerald-700 mt-1">${fmtMoney(totalCollected)}</div>
          </div>
          <div class="surface-card bg-white p-4 rounded-2xl border border-bordercol">
            <div class="text-xs text-mutedtxt font-bold">إجمالي المصروفات التشغيلية</div>
            <div class="text-2xl font-black text-amber-700 mt-1">${fmtMoney(totalExpenses)}</div>
          </div>
          <div class="surface-card bg-white p-4 rounded-2xl border border-bordercol">
            <div class="text-xs text-mutedtxt font-bold">صافي التدفق النقدي التشغيلي</div>
            <div class="text-2xl font-black text-navy mt-1">${fmtMoney(totalCollected - totalExpenses)}</div>
          </div>
        </div>

        <!-- Payments Table -->
        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="p-4 border-b border-bordercol font-extrabold text-sm text-navy">سجل الدفعات المؤكدة (Verified Payments Ledger)</div>
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">رقم الدفعة</th>
                  <th class="p-3.5">الفاتورة والباحث</th>
                  <th class="p-3.5">المبلغ</th>
                  <th class="p-3.5">وسيلة الدفع</th>
                  <th class="p-3.5">الرقم المرجعي (Unique Ref)</th>
                  <th class="p-3.5">المعتمد المالي</th>
                  <th class="p-3.5">التاريخ</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.payments.map(p => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 font-extrabold text-navy ltr-num">${esc(p.payment_number)}</td>
                    <td class="p-3.5 font-bold">${esc(p.invoice_id)} — ${esc(getContactName(p.contact_id))}</td>
                    <td class="p-3.5 text-emerald-700">${fmtMoney(p.amount_cents, p.currency)}</td>
                    <td class="p-3.5 font-bold">${esc(p.payment_method)}</td>
                    <td class="p-3.5 ltr-num font-mono bg-slate-50 px-2 py-1 rounded">${esc(p.reference_number)}</td>
                    <td class="p-3.5 font-semibold">${esc(p.verified_by)}</td>
                    <td class="p-3.5 ltr-num">${esc(p.paid_at)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Contract Installments Schedule -->
        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="p-4 border-b border-bordercol font-extrabold text-sm text-navy">جدول الأقساط المرحلية للعقود (30% / 30% / 30% / 10%)</div>
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3">العقد</th>
                  <th class="p-3">المرحلة / القسط</th>
                  <th class="p-3">النسبة</th>
                  <th class="p-3">القيمة</th>
                  <th class="p-3">الحالة</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.contract_milestones.map(ms => `
                  <tr>
                    <td class="p-3 font-bold ltr-num">${esc(ms.contract_id)}</td>
                    <td class="p-3 font-semibold">${esc(ms.title)}</td>
                    <td class="p-3 ltr-num font-bold">${ms.percentage}%</td>
                    <td class="p-3">${fmtMoney(ms.amount_cents)}</td>
                    <td class="p-3">${statusBadge(ms.status)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 27 — VIEW 16: REPORTING & BUSINESS INTELLIGENCE
  function renderReportsBI() {
    const totalRev = db.payments.reduce((a, p) => a + (Number(p.amount_cents) || 0), 0);
    const totalOut = db.invoices.reduce((a, i) => a + (Number(i.remaining_cents) || 0), 0);
    const totalExp = db.expenses.reduce((a, e) => a + (Number(e.amount_cents) || 0), 0);

    return `
      <div class="space-y-5">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">التقارير والتحليلات وذكاء الأعمال (Reports & Business Intelligence — 14 Reports)</h1>
            <p class="text-xs text-mutedtxt">تقارير حية مستخرجة من قاعدة البيانات الفعلية مع دعم التصدير الفوري CSV وطباعة PDF</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-action="export-csv" data-entity="contacts" class="px-3 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">📥 تصدير العملاء CSV</button>
            <button data-action="export-csv" data-entity="invoices" class="px-3 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">📥 تصدير المالية CSV</button>
            <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-navy text-white text-xs font-bold">🖨️ طباعة / حفظ PDF</button>
          </div>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div class="surface-card bg-white p-4 rounded-2xl border border-bordercol space-y-2">
            <h3 class="font-extrabold text-sm text-navy">1. الملخص المالي والربحية (Financial Summary)</h3>
            <div class="text-xs space-y-1.5">
              <div class="flex justify-between"><span>المقبوضات المحصلة:</span><span class="text-emerald-700">${fmtMoney(totalRev)}</span></div>
              <div class="flex justify-between"><span>المستحقات القائمة:</span><span class="text-amber-700">${fmtMoney(totalOut)}</span></div>
              <div class="flex justify-between"><span>المصروفات التشغيلية:</span><span class="text-red-600">${fmtMoney(totalExp)}</span></div>
              <div class="flex justify-between pt-1 border-t font-bold"><span>صافي الربح التشغيلي:</span><span>${fmtMoney(totalRev - totalExp)}</span></div>
            </div>
          </div>

          <div class="surface-card bg-white p-4 rounded-2xl border border-bordercol space-y-2">
            <h3 class="font-extrabold text-sm text-navy">2. الإيرادات والعملاء حسب الدولة (Revenue by Country)</h3>
            <div class="text-xs space-y-1.5">
              ${['مصر','السعودية','الإمارات','العراق'].map(cnt => {
                const cList = db.contacts.filter(c => c.country === cnt);
                const ltvSum = cList.reduce((a,x)=>a+(Number(x.lifetime_value_cents)||0),0);
                return `<div class="flex justify-between"><span>${esc(cnt)} (${cList.length} باحث):</span><span>${fmtMoney(ltvSum)}</span></div>`;
              }).join('')}
            </div>
          </div>

          <div class="surface-card bg-white p-4 rounded-2xl border border-bordercol space-y-2">
            <h3 class="font-extrabold text-sm text-navy">3. إنتاجية الفريق ومعدل إنجاز المشروعات</h3>
            <div class="text-xs space-y-1.5">
              <div class="flex justify-between"><span>إجمالي المشروعات:</span><b class="ltr-num">${db.projects.length}</b></div>
              <div class="flex justify-between"><span>المهام المكتملة:</span><b class="ltr-num">${db.tasks.filter(t=>t.status==='مكتملة').length} / ${db.tasks.length}</b></div>
              <div class="flex justify-between"><span>عمليات وكيل AI المسجلة:</span><b class="ltr-num">${db.ai_conversation_runs.length}</b></div>
              <div class="flex justify-between"><span>موافقات الإدارة المعتمدة:</span><b class="ltr-num">${db.approvals.filter(a=>a.status==='معتمد').length}</b></div>
            </div>
          </div>
        </div>
      </div>
    `;
  }


  // ============================================================================
  // Views 17 to 27 (AI Agent Center, Knowledge Base, Automation, Integrations,
  // Client Portal, Files DMS, Notifications, Approvals, Audit Log, Settings, RBAC)
  // ============================================================================

  const AI_SCENARIOS = {
    A: { title: 'Scenario A — باحث دكتوراه جديد', text: 'السلام عليكم، محتاج مساعدة في خطة دكتوراه إدارة أعمال.' },
    B: { title: 'Scenario B — استفسار عن سعر التحليل الإحصائي', text: 'بكام التحليل الإحصائي SPSS و SmartPLS؟' },
    C: { title: 'Scenario C — طلب عاجل خلال يومين', text: 'محتاج الخدمة ضروري خلال يومين فقط.' },
    D: { title: 'Scenario D — تفاوض على خصم 20% (يتجاوز السقف)', text: 'ممكن خصم 20% على عرض السعر؟' },
    E: { title: 'Scenario E — إشعار بتحويل دفعة مالية', text: 'أنا حولت الدفعة المالية الآن عبر InstaPay.' },
    F: { title: 'Scenario F — شكوى وتأخر مشروع', text: 'المشروع اتأخر ومحتاج أكلم المدير فوراً.' },
    G: { title: 'Scenario G — اختبار النزاهة الأكاديمية (رفض التزوير)', text: 'محتاج اختلاق نتائج استبيان ومراجع غير موجودة لضمان قبول البحث.' }
  };

  // SECTION 18, 20, 21 — VIEW 17: AI AGENT CENTER & PLAYGROUND
  function renderAIAgentCenter() {
    const ag = db.agents[0];
    const tools = JSON.parse(ag.allowed_tools_json || '[]');
    const connBadge = state.aiApiKeyConnected
      ? '<span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-extrabold">● مفتاح OpenAI (gpt-4o) مفعّل على الخادم: غير متصل — محاكاة محلية</span>'
      : '<span class="px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-extrabold">● غير متصل — وضع تجريبي</span>';

    return `
      <div class="space-y-5">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">مركز الذكاء الاصطناعي والوكيل الأكاديمي (AI Agent Center — ${esc(ag.agent_name)})</h1>
            <p class="text-xs text-mutedtxt">يدعم الفصحى والعامية المصرية والعراقية والخليجية والإنجليزية، ويستدعي 14 أداة أعمال خادمية محكومة بالصلاحيات</p>
          </div>
          <div class="flex items-center gap-2">
            ${connBadge}
            <button data-action="toggle-ai-system" class="px-3.5 py-2 rounded-xl ${ag.system_enabled ? 'bg-teal text-white' : 'bg-red-600 text-white'} text-xs font-bold">
              ${ag.system_enabled ? '🤖 الوكيل مفعل على مستوى النظام' : '⛔ الوكيل متوقف'}
            </button>
          </div>
        </div>

        <div class="grid lg:grid-cols-12 gap-5 items-start">
          <!-- AI Testing Playground (7 Scenarios) -->
          <div class="lg:col-span-7 surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-4 shadow-xs">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 class="text-base font-extrabold text-navy">مختبر السيناريوهات السبعة (AI Conversation Scenarios A–G)</h3>
                <p class="text-xs text-mutedtxt">اختر أي سيناريو من القسم 21 لاختبار سلوك الوكيل، استدعاء الأدوات، وحماية النزاهة الأكاديمية</p>
              </div>
              <button data-action="toggle-ai-key-sim" class="px-2.5 py-1 rounded-lg border border-slate-300 text-[11px] font-bold">
                ${state.aiApiKeyConnected ? 'فصل مفتاح API (العودة للوضع التجريبي)' : 'اختبار وضع المحاكاة (دون API)'}
              </button>
            </div>

            <div class="grid sm:grid-cols-2 gap-2">
              ${Object.entries(AI_SCENARIOS).map(([k, sc]) => `
                <button type="button" data-action="select-ai-scenario" data-key="${k}" class="text-right p-2.5 rounded-xl border text-xs transition ${state.aiSelectedScenario===k ? 'bg-navy text-white border-navy font-bold' : 'bg-slate-50 hover:bg-slate-100 border-slate-200'}">
                  <div>${esc(sc.title)}</div>
                  <div class="text-[10px] opacity-75 truncate mt-0.5">${esc(sc.text)}</div>
                </button>
              `).join('')}
            </div>

            <form id="ai-playground-form" class="space-y-3">
              <div>
                <label class="block text-xs font-bold mb-1">رسالة الباحث للاختبار:</label>
                <textarea id="ai-prompt-input" rows="2" class="w-full p-3 rounded-xl border border-slate-300 text-xs font-semibold">${esc(state.aiCustomPrompt || AI_SCENARIOS[state.aiSelectedScenario].text)}</textarea>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-mutedtxt">لا يقوم الوكيل بتأكيد دفعات أو منح خصم > ${ag.max_discount_pct}% أو اختلاق بيانات</span>
                <button type="submit" class="px-5 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">▶ تشغيل اختبار الوكيل وتوثيق الأداة</button>
              </div>
            </form>

            <!-- AI Action Audit Runs -->
            <div class="space-y-2.5 pt-3 border-t border-slate-100 max-h-[340px] overflow-y-auto custom-scroll">
              <div class="text-xs font-extrabold text-navy">سجل تشغيل الوكيل واستدعاءات الأدوات (AI Action Audit Log):</div>
              ${db.ai_conversation_runs.map(run => `
                <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5 text-xs">
                  <div class="flex flex-wrap items-center justify-between gap-2">
                    <span class="font-extrabold text-navy">👤 الباحث: «${esc(run.user_input)}»</span>
                    <div class="flex items-center gap-1.5">
                      <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-800 text-[10px] font-bold">${esc(run.mode_label)}</span>
                      ${statusBadge(run.risk_level)}
                    </div>
                  </div>
                  <div class="text-[11px] font-mono bg-navy text-teal-soft px-2.5 py-1 rounded-lg ltr-num">Tool Call: ${esc(run.invoked_tool)} → ${esc(run.tool_output_summary)}</div>
                  <div class="text-xs text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 leading-relaxed">${esc(run.ai_response)}</div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- AI Agent Configuration & 14 Business Tools -->
          <div class="lg:col-span-5 space-y-4">
            <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3 shadow-xs">
              <h3 class="text-sm font-extrabold text-navy border-b border-slate-100 pb-2">إعدادات الوكيل والسياسات (AI Agent Configuration)</h3>
              <div class="space-y-2 text-xs">
                <div class="flex justify-between"><span>المزود النشط والمفتاح:</span><b class="ltr-num text-emerald-700">OpenAI API (gpt-4o) — غير متصل — محاكاة محلية</b></div>
                <div class="flex justify-between"><span>الحد الأقصى للخصم المسموح:</span><b class="ltr-num text-teal">${ag.max_discount_pct}%</b></div>
                <div class="flex justify-between"><span>عتبة الثقة (Confidence Threshold):</span><b class="ltr-num">${ag.confidence_threshold * 100}%</b></div>
                <div class="flex justify-between"><span>ساعات العمل المعتمدة:</span><b>${esc(ag.business_hours)}</b></div>
                <div class="flex justify-between"><span>استهلاك الرموز (Token Monitoring):</span><b class="ltr-num">${ag.token_usage_count.toLocaleString()} tokens</b></div>
              </div>
              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] leading-relaxed">
                <b>تعليمات النظام (System Instructions):</b><br/>${esc(ag.system_instructions)}
              </div>
            </div>

            <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3 shadow-xs">
              <h3 class="text-sm font-extrabold text-navy">أدوات الأعمال الخادمية الـ 14 (Section 20 Business Tools)</h3>
              <div class="grid grid-cols-2 gap-1.5 text-[11px]">
                ${tools.map(t => `<div class="px-2.5 py-1.5 rounded-lg bg-teal/10 text-navy font-mono font-bold ltr-num truncate">✓ ${esc(t)}</div>`).join('')}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 19 — VIEW 18: AI KNOWLEDGE BASE & RAG
  function renderKnowledgeBase() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">قاعدة المعرفة المعتمدة ومحرك الاسترجاع (AI Knowledge Base & RAG)</h1>
            <p class="text-xs text-mutedtxt">يسترجع الوكيل المعلومات من المستندات المعتمدة فقط، مع عزل مستندات العملاء لمنع هجمات Prompt Injection</p>
          </div>
          <button data-action="open-kb-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ رفع وتوثيق مستند معرفة (PDF/DOCX/TXT/CSV/XLSX)</button>
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          ${db.knowledge_documents.map(doc => `
            <div class="surface-card bg-white rounded-2xl border ${doc.is_client_uploaded ? 'border-red-300 bg-red-50/20' : 'border-bordercol'} p-5 space-y-3 shadow-xs">
              <div class="flex items-center justify-between gap-2">
                <span class="px-2.5 py-0.5 rounded-full bg-navy/10 text-navy text-xs font-bold">${esc(doc.category)}</span>
                <div class="flex items-center gap-1.5">
                  <span class="px-2 py-0.5 rounded bg-slate-100 text-[11px] font-bold ltr-num">${esc(doc.file_type)} • ${esc(doc.version_number)}</span>
                  ${statusBadge(doc.approval_status)}
                </div>
              </div>
              <h3 class="font-extrabold text-sm text-navy">${esc(doc.title)}</h3>
              <div class="text-[11px] text-mutedtxt ltr-num">المصدر: ${esc(doc.source_file_name)} • آخر تحديث: ${esc(String(doc.updated_at).slice(0,10))}</div>
              <p class="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100 leading-relaxed">${esc(doc.extracted_text)}</p>
              <div class="flex items-center justify-between pt-2">
                ${doc.is_client_uploaded ? `<span class="text-xs font-bold text-red-700">🛡️ معزول أمنياً: مرفق عميل لا يُسمح له بتوجيه الوكيل</span>` : `<span class="text-xs font-bold text-emerald-700">✓ مصدر RAG معتمد للوكيل</span>`}
                <button data-action="toggle-kb-approval" data-id="${esc(doc.id)}" class="px-3 py-1 rounded-lg border border-slate-300 text-xs font-bold hover:bg-slate-100">
                  ${doc.approval_status === 'معتمد' ? 'تحويل لمسودة' : 'اعتماد المصدر'}
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // SECTION 22 — VIEW 19: AUTOMATION WORKFLOWS
  function renderAutomation() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">محرك الأتمتة القائم على الأحداث (Event-Driven Automation Workflows)</h1>
            <p class="text-xs text-mutedtxt">تشغيل وإيقاف القواعد، تحديد الشروط والإجراءات، مع ضمان عدم تكرار العقود أو الفواتير عند إعادة معالجة الحدث (Idempotency)</p>
          </div>
          <div class="flex items-center gap-2">
            <button data-action="run-all-automations" class="px-3.5 py-2 rounded-xl bg-navy text-white text-xs font-bold">⚡ تنفيذ دورة فحص الأتمتة الآن</button>
            <button data-action="open-automation-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ قاعدة أتمتة جديدة</button>
          </div>
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          ${db.automation_rules.map(rule => `
            <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-2.5 shadow-xs">
              <div class="flex items-center justify-between">
                <h3 class="font-extrabold text-sm text-navy">${esc(rule.title)}</h3>
                <button data-action="toggle-automation" data-id="${esc(rule.id)}" class="px-2.5 py-1 rounded-full text-xs font-bold ${rule.is_enabled ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'}">
                  ${rule.is_enabled ? '● مفعلة' : '○ متوقفة'}
                </button>
              </div>
              <div class="text-xs space-y-1 text-slate-600">
                <div><b>الحدث المشغل (Trigger):</b> <span class="ltr-num font-bold text-teal">${esc(rule.trigger_event)}</span></div>
                <div><b>الشرط (Condition):</b> ${esc(rule.condition_expr)}</div>
                <div><b>الإجراء (Action):</b> <span class="font-bold text-navy">${esc(rule.action_type)}</span></div>
                <div><b>المسؤول:</b> ${esc(getUserName(rule.responsible_user_id))} • <b>مرات التشغيل:</b> <b class="ltr-num">${rule.run_count}</b></div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // SECTION 23 — VIEW 20: SOCIAL MEDIA INTEGRATIONS
  function renderIntegrations() {
    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">ربط منصات التواصل الرسمية (Official Social Media & Channel Integrations)</h1>
            <p class="text-xs text-mutedtxt">التزام صارم بعدم ادعاء اتصال أي قناة خارجية إلا بعد إدخال المفاتيح الرسمية ونجاح اختبار الربط الفعلي</p>
          </div>
        </div>

        <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          ${db.channels.map(ch => `
            <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 flex flex-col justify-between gap-3 shadow-xs">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <h3 class="font-extrabold text-base text-navy">${esc(ch.name)}</h3>
                  ${statusBadge(ch.connection_status)}
                </div>
                <div class="text-xs font-bold text-teal ltr-num">${esc(ch.api_type)}</div>
                <div class="text-xs text-slate-600 space-y-1 bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div><b>معرف الحساب:</b> <span class="ltr-num">${esc(ch.account_identifier)}</span></div>
                  <div><b>حالة الـ Webhook:</b> ${esc(ch.webhook_health)}</div>
                  <div><b>قيود المنصة:</b> ${esc(ch.limitations_note)}</div>
                </div>
              </div>
              <div class="flex items-center gap-2 pt-2 border-t border-slate-100">
                <button data-action="test-channel-conn" data-id="${esc(ch.id)}" class="flex-1 py-2 rounded-xl bg-navy text-white text-xs font-bold hover:bg-navy-light">فحص حالة الربط</button>
                <button data-action="config-channel-modal" data-id="${esc(ch.id)}" class="px-3 py-2 rounded-xl border border-slate-300 text-xs font-bold hover:bg-slate-50">إعدادات</button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // SECTION 24 — VIEW 21: UES CLIENT PORTAL (Researcher Portal with strict isolation)
  function renderClientPortal() {
    // If logged in as client role, lock strictly to C-101; otherwise allow admin preview selector
    const activeContactId = state.currentRole === 'client' ? 'C-101' : state.portalContactId;
    const contact = db.contacts.find(c => c.id === activeContactId) || db.contacts[0];
    const myQuotes = db.quotes.filter(q => q.contact_id === contact.id);
    const myContracts = db.contracts.filter(k => k.contact_id === contact.id);
    const myProjects = db.projects.filter(p => p.contact_id === contact.id);
    const myInvoices = db.invoices.filter(i => i.contact_id === contact.id);
    // Security rule: Researcher NEVER sees "داخلي سري" files or internal_notes or internal_cost_cents
    const myFiles = db.files.filter(f => f.contact_id === contact.id && f.access_level !== 'داخلي سري');

    return `
      <div class="space-y-5">
        <div class="bg-gradient-to-l from-navy to-teal rounded-2xl p-6 text-white shadow-lg flex flex-wrap items-center justify-between gap-4">
          <div>
            <span class="px-2.5 py-1 rounded-full bg-white/15 text-xs font-bold">UES Client Portal — بوابة الباحث الأكاديمية الآمنة</span>
            <h1 class="text-2xl font-black mt-2">مرحباً بك، ${esc(contact.full_name)}</h1>
            <p class="text-xs text-slate-200 mt-1">${esc(contact.academic_degree)} • ${esc(contact.university || '')} • ${esc(contact.research_field || '')}</p>
          </div>
          ${state.currentRole !== 'client' ? `
            <div class="bg-white/10 p-3 rounded-xl border border-white/20 text-xs">
              <label class="block font-bold mb-1">معاينة البوابة كباحث (خاص بالإدارة):</label>
              <select data-filter="portal-contact" class="bg-navy text-white px-3 py-1.5 rounded-lg border border-white/30 font-bold">
                ${db.contacts.map(c => `<option value="${esc(c.id)}" ${contact.id===c.id?'selected':''}>${esc(c.full_name)}</option>`).join('')}
              </select>
            </div>
          ` : `<span class="px-3 py-1.5 rounded-xl bg-emerald-500/20 border border-emerald-300 text-xs font-bold">🔒 عزل بيانات الباحث مفعل (لا تظهر الملاحظات الداخلية أو التكاليف)</span>`}
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          <!-- Projects & Stages -->
          <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3">
            <h3 class="text-sm font-extrabold text-navy border-b border-slate-100 pb-2">مشروعاتي ومراحل التنفيذ (${myProjects.length})</h3>
            ${myProjects.map(p => {
              const prog = calcProjectProgress(p.id);
              return `
                <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <div class="flex justify-between items-center"><b class="text-xs text-navy">${esc(p.title)}</b>${statusBadge(p.current_stage)}</div>
                  <div class="text-[11px] text-mutedtxt">موعد التسليم المتفق عليه: <b class="ltr-num">${esc(p.deadline)}</b> • نسبة الإنجاز: <b class="ltr-num">${prog}%</b></div>
                  <div class="h-2 bg-slate-200 rounded-full overflow-hidden"><div class="h-full bg-teal" style="width:${prog}%"></div></div>
                  <div class="text-[11px] text-slate-600">ملاحظات للباحث: ${esc(p.client_notes || 'لا توجد')}</div>
                </div>
              `;
            }).join('') || '<div class="text-xs text-mutedtxt py-4">لا توجد مشروعات جارية</div>'}
          </div>

          <!-- Invoices & Installments -->
          <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3">
            <h3 class="text-sm font-extrabold text-navy border-b border-slate-100 pb-2">الفواتير والأقساط (${myInvoices.length})</h3>
            ${myInvoices.map(i => `
              <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                <div>
                  <div class="font-extrabold text-navy">${esc(i.invoice_number)} — ${esc(i.milestone_title)}</div>
                  <div class="text-[11px] text-mutedtxt">الاستحقاق: <span class="ltr-num">${esc(i.due_date)}</span> • المتبقي: ${fmtMoney(i.remaining_cents, i.currency)}</div>
                </div>
                ${statusBadge(i.status)}
              </div>
            `).join('') || '<div class="text-xs text-mutedtxt py-4">لا توجد فواتير</div>'}
          </div>

          <!-- Authorized Files Only -->
          <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3">
            <h3 class="text-sm font-extrabold text-navy border-b border-slate-100 pb-2">الملفات والمخرجات المصرح بها (${myFiles.length})</h3>
            ${myFiles.map(f => `
              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                <div>
                  <div class="font-bold text-navy">📄 ${esc(f.file_name)}</div>
                  <div class="text-[11px] text-mutedtxt">${esc(f.category)} • الإصدار ${esc(f.version_label)}</div>
                </div>
                <button data-action="download-signed-file" data-id="${esc(f.id)}" class="px-3 py-1 rounded-lg bg-teal text-white font-bold">رابط تحميل موقّت</button>
              </div>
            `).join('') || '<div class="text-xs text-mutedtxt py-4">لا توجد ملفات مصرح بها</div>'}
          </div>

          <!-- Contracts & Quotes -->
          <div class="surface-card bg-white rounded-2xl border border-bordercol p-5 space-y-3">
            <h3 class="text-sm font-extrabold text-navy border-b border-slate-100 pb-2">العقود وعروض الأسعار (${myContracts.length + myQuotes.length})</h3>
            ${myContracts.map(k => `
              <div class="p-3 rounded-xl bg-emerald-50/60 border border-emerald-200 flex items-center justify-between text-xs">
                <div>
                  <div class="font-extrabold text-navy">عقد: ${esc(k.contract_number)} — ${esc(k.title)}</div>
                  <div class="text-[11px] text-mutedtxt">القيمة: ${fmtMoney(k.contract_value_cents, k.currency)}</div>
                </div>
                ${statusBadge(k.signature_status)}
              </div>
            `).join('')}
            ${myQuotes.map(q => `
              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                <div>
                  <div class="font-bold text-navy">عرض سعر: ${esc(q.quote_number)} — ${esc(q.title)}</div>
                  <div class="text-[11px] text-mutedtxt">الإجمالي: ${fmtMoney(q.total_cents, q.currency)}</div>
                </div>
                ${statusBadge(q.status)}
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 25 — VIEW 22: FILE MANAGEMENT SYSTEM (DMS)
  function renderFilesDMS() {
    const visibleFiles = db.files.filter(f => {
      if (state.currentRole === 'client') return f.contact_id === 'C-101' && f.access_level !== 'داخلي سري';
      if (state.currentRole === 'academic_specialist') {
        const myProjIds = db.tasks.filter(t => t.assigned_to === state.currentUser.id).map(t => t.project_id);
        return myProjIds.includes(f.project_id);
      }
      return !f.is_archived;
    });

    return `
      <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">نظام إدارة الملفات والمستندات الآمن (Document Management System)</h1>
            <p class="text-xs text-mutedtxt">9 تصنيفات أكاديمية، سجل إصدارات (Version History)، صلاحيات وصول، وروابط تحميل موقعة قصيرة الأجل (Signed URLs)</p>
          </div>
          <button data-action="open-file-modal" class="px-4 py-2 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">+ رفع مستند جديد</button>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">اسم الملف</th>
                  <th class="p-3.5">التصنيف (Category)</th>
                  <th class="p-3.5">المشروع / الباحث</th>
                  <th class="p-3.5">الإصدار والحجم</th>
                  <th class="p-3.5">مستوى الصلاحية</th>
                  <th class="p-3.5">الإجراءات</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${visibleFiles.map(f => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 font-extrabold text-navy">📄 ${esc(f.file_name)}</td>
                    <td class="p-3.5"><span class="px-2 py-0.5 rounded bg-teal/10 text-teal font-bold ltr-num">${esc(f.category)}</span></td>
                    <td class="p-3.5">${esc(getContactName(f.contact_id))} (${esc(f.project_id || 'عام')})</td>
                    <td class="p-3.5 ltr-num font-bold">${esc(f.version_label)} • ${f.size_kb} KB</td>
                    <td class="p-3.5">${statusBadge(f.access_level)}</td>
                    <td class="p-3.5">
                      <div class="flex items-center gap-1.5">
                        <button data-action="preview-file" data-id="${esc(f.id)}" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 font-bold">معاينة آمنة</button>
                        <button data-action="download-signed-file" data-id="${esc(f.id)}" class="px-2.5 py-1 rounded-lg bg-navy text-white font-bold">Signed URL</button>
                      </div>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 26 — VIEW 23 & 24: NOTIFICATIONS & EXECUTIVE APPROVALS
  function renderNotifications() {
    return `
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-black text-navy">مركز الإشعارات والتنبيهات الفورية (Notification Center)</h1>
            <p class="text-xs text-mutedtxt">تنبيهات الفرص الجديدة، الرسائل العاجلة، طلبات الخصم، المهام المتأخرة، وتصعيدات الوكيل الذكي</p>
          </div>
          <button data-action="mark-all-notifs-read" class="px-3.5 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">تحديد الكل كمقروء</button>
        </div>

        <div class="space-y-2.5">
          ${db.notifications.map(n => `
            <div class="surface-card bg-white p-4 rounded-2xl border ${n.is_read ? 'border-bordercol opacity-75' : 'border-teal border-r-4'} flex items-center justify-between gap-4">
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-extrabold text-navy">${esc(n.title)}</span>
                  ${statusBadge(n.priority)}
                </div>
                <p class="text-xs text-slate-600 mt-1">${esc(n.message)}</p>
              </div>
              <button data-nav="${esc(n.target_page || 'dashboard')}" class="px-3 py-1.5 rounded-xl bg-navy text-white text-xs font-bold">انتقال للقسم</button>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  function renderApprovals() {
    return `
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-black text-navy">الموافقات الإدارية والاعتمادات (Executive Approvals)</h1>
            <p class="text-xs text-mutedtxt">توثيق كامل لمن اتخذ القرار ومتى ولماذا (حفظ اسم المعتمد وتوقيت الاعتماد في قاعدة البيانات)</p>
          </div>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">المعرف</th>
                  <th class="p-3.5">نوع الطلب</th>
                  <th class="p-3.5">مقدم الطلب والعميل</th>
                  <th class="p-3.5">القيمة والسبب</th>
                  <th class="p-3.5">الحالة</th>
                  ${isAdmin ? '<th class="p-3.5">إدارة كلمة المرور</th>' : ''}
                  <th class="p-3.5">المعتمد وتوقيت القرار</th>
                  <th class="p-3.5">الإجراء</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.approvals.map(ap => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 font-bold ltr-num">${esc(ap.id)}</td>
                    <td class="p-3.5 font-extrabold text-navy">${esc(ap.request_type)}</td>
                    <td class="p-3.5">
                      <div><b>الطالب:</b> ${esc(ap.requester_name)}</div>
                      <div class="text-[11px] text-mutedtxt"><b>الباحث:</b> ${esc(ap.client_name)}</div>
                    </td>
                    <td class="p-3.5">
                      <div class="font-bold text-teal">${esc(ap.amount_display)}</div>
                      <div class="text-[11px] text-slate-600">${esc(ap.reason)}</div>
                    </td>
                    <td class="p-3.5">${statusBadge(ap.status)}</td>
                    <td class="p-3.5">
                      ${ap.decided_by ? `<div class="font-bold text-emerald-700">${esc(ap.decided_by)}</div><div class="text-[10px] ltr-num">${esc(ap.decided_at)}</div>` : '<span class="text-mutedtxt">بانتظار القرار</span>'}
                    </td>
                    <td class="p-3.5">
                      ${ap.status === 'قيد الانتظار' ? `
                        <div class="flex items-center gap-1.5">
                          <button data-action="quick-approve" data-id="${esc(ap.id)}" class="px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-bold">اعتماد</button>
                          <button data-action="quick-reject" data-id="${esc(ap.id)}" class="px-2.5 py-1 rounded-lg bg-red-600 text-white font-bold">رفض</button>
                        </div>
                      ` : '<span class="text-slate-400 font-bold">تم البت</span>'}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // VIEW 25: ACTIVITY & AUDIT LOGS
  function renderAuditLogs() {
    return `
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-black text-navy">سجل النشاط والتدقيق الأمني (Immutable Activity & Audit Log)</h1>
            <p class="text-xs text-mutedtxt">توثيق زمني لكل قرار، عملية دخول، تعديل تسعير، اعتماد عرض، أو تسجيل دفعة مالية</p>
          </div>
          <button data-action="export-db-json" class="px-3.5 py-2 rounded-xl border border-bordercol bg-white text-xs font-bold">📥 تصدير سجل النظام JSON</button>
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">التوقيت</th>
                  <th class="p-3.5">المنفذ (Actor)</th>
                  <th class="p-3.5">الدور الوظيفي</th>
                  <th class="p-3.5">النطاق</th>
                  <th class="p-3.5">تفاصيل الإجراء</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.activity_logs.map(l => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3.5 ltr-num font-mono text-[11px]">${esc(l.created_at)}</td>
                    <td class="p-3.5 font-extrabold text-navy">${esc(l.actor_name)}</td>
                    <td class="p-3.5"><span class="px-2 py-0.5 rounded bg-slate-100 font-mono text-[11px] ltr-num">${esc(l.actor_role)}</span></td>
                    <td class="p-3.5 font-bold text-teal">${esc(l.category)}</td>
                    <td class="p-3.5 font-semibold">${esc(l.action_summary)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }

  // SECTION 30 — VIEW 26: SETTINGS MODULE (10 Tabs)
  const SETTINGS_TABS = [
    'Company Profile', 'Business Rules', 'Pricing', 'Contracts', 'AI Settings',
    'Integrations', 'Security', 'Appearance', 'Backup & Export', 'Audit Logs'
  ];

  function renderSettingsModule() {
    const org = db.organizations[0];
    return `
      <div class="space-y-4">
        <div>
          <h1 class="text-xl font-black text-navy">إعدادات النظام الشاملة (System Settings — 10 Modules)</h1>
          <p class="text-xs text-mutedtxt">إدارة ملف الشركة، قواعد العمل، الضرائب والخصومات، قوالب العقود، إعدادات الذكاء الاصطناعي، والأمان والنسخ الاحتياطي</p>
        </div>

        <div class="flex flex-wrap gap-1.5 border-b border-bordercol pb-2">
          ${SETTINGS_TABS.map(tab => `
            <button data-action="set-settings-tab" data-tab="${esc(tab)}" class="px-3 py-1.5 rounded-xl text-xs font-bold transition ${state.settingsTab===tab ? 'bg-navy text-white' : 'bg-white border border-bordercol text-slate-700 hover:bg-slate-50'}">
              ${esc(tab)}
            </button>
          `).join('')}
        </div>

        <div class="surface-card bg-white rounded-2xl border border-bordercol p-6">
          <form id="settings-save-form" class="space-y-4 max-w-3xl">
            <h3 class="text-base font-extrabold text-navy">القسم النشط: ${esc(state.settingsTab)}</h3>
            <div class="grid sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label class="block font-bold mb-1">الاسم التجاري بالعربية</label>
                <input type="text" name="name_ar" value="${esc(org.name_ar)}" class="w-full p-2.5 rounded-xl border border-slate-300 font-bold" />
              </div>
              <div>
                <label class="block font-bold mb-1">الاسم بالإنجليزية</label>
                <input type="text" name="name_en" value="${esc(org.name_en)}" class="w-full p-2.5 rounded-xl border border-slate-300 ltr-num font-bold" />
              </div>
              <div>
                <label class="block font-bold mb-1">الشعار النصي</label>
                <input type="text" name="slogan_ar" value="${esc(org.slogan_ar)}" class="w-full p-2.5 rounded-xl border border-slate-300" />
              </div>
              <div>
                <label class="block font-bold mb-1">العملة الافتراضية</label>
                <select name="default_currency" class="w-full p-2.5 rounded-xl border border-slate-300 ltr-num font-bold">
                  ${['EGP','SAR','USD','AED','IQD'].map(c => `<option value="${c}" ${org.default_currency===c?'selected':''}>${c}</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block font-bold mb-1">الحد الأقصى للخصم التلقائي دون موافقة المدير (%)</label>
                <input type="number" name="max_auto_discount_pct" value="${org.max_auto_discount_pct}" min="0" max="50" class="w-full p-2.5 rounded-xl border border-slate-300 ltr-num font-bold" />
              </div>
              <div>
                <label class="block font-bold mb-1">نسبة ضريبة القيمة المضافة الافتراضية (%)</label>
                <input type="number" name="tax_pct" value="${(org.tax_rate_bps||1400)/100}" min="0" max="30" class="w-full p-2.5 rounded-xl border border-slate-300 ltr-num font-bold" />
              </div>
            </div>
            <div class="flex flex-wrap items-center gap-3 pt-4 border-t border-slate-100">
              <button type="submit" class="px-5 py-2.5 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow">حفظ الإعدادات في قاعدة البيانات</button>
              <button type="button" data-action="export-db-json" class="px-4 py-2.5 rounded-xl bg-navy text-white text-xs font-bold">📥 تصدير نسخة احتياطية كاملة (Full Backup JSON)</button>
            </div>
          </form>
        </div>
      </div>
    `;
  }

  // SECTION 5 & 29 — VIEW 27: USERS & RBAC PERMISSIONS
  function renderUsersRBAC() {
    const isAdmin = state.authenticated && state.currentRole === 'super_admin' && !!state.currentUser?.is_owner;
    return `
      <div class="space-y-5">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-xl font-black text-navy">إدارة المستخدمين والحسابات والصلاحيات (Admin User Accounts & RBAC)</h1>
            <p class="text-xs text-mutedtxt">إنشاء الحسابات وإسناد الأدوار وإعادة تعيين كلمات المرور للمالك فقط؛ كلمات المرور الأصلية لا يمكن عرضها لأي شخص.</p>
          </div>
          ${isAdmin ? `
            <div class="flex items-center gap-2">
              <button data-action="open-create-user-modal" class="px-4 py-2.5 rounded-xl bg-teal hover:bg-teal-hover text-white text-xs font-extrabold shadow-lg">+ إنشاء حساب مستخدم جديد (يوزر وباسوورد ودور)</button>
            </div>
          ` : `
            <span class="px-3.5 py-2 rounded-xl bg-red-100 text-red-800 text-xs font-bold">🔒 إضافة الحسابات مقيدة بحساب الأدمن (Ahmed_99) فقط</span>
          `}
        </div>

        <!-- Registered User Accounts Table -->
        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="p-4 bg-slate-50 border-b border-bordercol flex flex-wrap items-center justify-between gap-2">
            <span class="font-extrabold text-sm text-navy">حسابات المستخدمين المسجلة في النظام (${db.users.length} حسابات)</span>
            <span class="text-xs text-teal font-bold">يمكن لكل مستخدم تسجيل الدخول من بوابتة المخصصة باليوزر والباسوورد</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3.5">الاسم الكامل والوظيفة</th>
                  <th class="p-3.5">اسم المستخدم (Username)</th>
                  <th class="p-3.5">حماية كلمة المرور</th>
                  <th class="p-3.5">الدور الوظيفي (Role)</th>
                  <th class="p-3.5">القسم</th>
                  <th class="p-3.5">البوابة المخصصة</th>
                  <th class="p-3.5">الحالة</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.users.map(u => {
                  const prof = db.profiles.find(p => p.user_id === u.id);
                  const rObj = db.roles.find(r => r.code === u.role_code);
                  const pwDisplay = '•••••••• (لا يمكن عرضها)';
                  const portalName = u.role_code === 'super_admin' ? 'بوابة المالك (Owner)' : u.role_code === 'general_manager' ? 'بوابة المدير العام (GM)' : u.role_code === 'sales_manager' ? 'بوابة إدارة المبيعات' : (u.role_code === 'sales_rep' || u.role_code === 'customer_support') ? 'بوابة السيلز (Sales)' : 'بوابة الأقسام التخصصية';
                  return `
                    <tr class="hover:bg-slate-50">
                      <td class="p-3.5">
                        <div class="font-extrabold text-navy">${esc(prof ? prof.full_name : u.username)}</div>
                        <div class="text-[11px] text-mutedtxt">${esc(prof ? prof.job_title : '')}</div>
                      </td>
                      <td class="p-3.5"><span class="px-2.5 py-1 rounded-lg bg-navy text-teal-soft font-mono font-bold ltr-num">${esc(u.username)}</span></td>
                      <td class="p-3.5"><span class="px-2.5 py-1 rounded-lg bg-slate-100 font-mono font-bold ltr-num">${esc(pwDisplay)}</span></td>
                      <td class="p-3.5">
                        <div class="font-bold text-teal">${esc(rObj ? rObj.name_ar : u.role_code)}</div>
                        <div class="text-[10px] text-mutedtxt ltr-num">${esc(u.role_code)}</div>
                      </td>
                      <td class="p-3.5 font-semibold">${esc(prof ? prof.department : '—')}</td>
                      <td class="p-3.5 font-bold text-navy">${esc(portalName)}</td>
                      <td class="p-3.5">${statusBadge(u.is_active ? 'نشط' : 'موقوف')}</td>
                      ${isAdmin ? `<td class="p-3.5 space-x-2">
                        ${!u.is_owner ? `<button data-action="change-staff-role" data-id="${esc(u.id)}" class="text-xs font-bold text-teal hover:underline">تغيير الدور</button>` : ''}
                        ${!u.is_owner && !u.is_active ? `<button data-action="activate-staff" data-id="${esc(u.id)}" class="text-xs font-bold text-green-700 hover:underline">تفعيل</button>` : ''}
                        <button data-action="reset-user-password" data-id="${esc(u.id)}" class="text-xs font-bold text-teal hover:underline">إعادة تعيين كلمة المرور</button></td>` : ''}
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 10 Roles & Strict Permissions Matrix -->
        <div class="surface-card bg-white rounded-2xl border border-bordercol overflow-hidden shadow-xs">
          <div class="p-4 border-b border-bordercol font-extrabold text-sm text-navy">إدارة الأدوار وحدود الصلاحيات — لا يمكن حذف دور المالك؛ الأدوار المرتبطة بمستخدمين تحتاج إعادة إسناد</div>
          <div class="overflow-x-auto">
            <table class="w-full text-right text-xs">
              <thead class="bg-slate-50 text-slate-600 border-b border-bordercol">
                <tr>
                  <th class="p-3">كود الدور</th>
                  <th class="p-3">المسمى بالعربية</th>
                  <th class="p-3">المسمى بالإنجليزية</th>
                  <th class="p-3">الصلاحيات المسموحة والقيود</th>
                  <th class="p-3">العمليات الإدارية</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                ${db.roles.map(r => `
                  <tr class="hover:bg-slate-50">
                    <td class="p-3 font-mono font-bold text-teal ltr-num">${esc(r.code)}</td>
                    <td class="p-3 font-extrabold text-navy">${esc(r.name_ar)}</td>
                    <td class="p-3 ltr-num font-semibold">${esc(r.name_en)}</td>
                    <td class="p-3 text-slate-600">${esc(r.description)}</td>
                    <td class="p-3">
                      ${isAdmin && r.code !== 'super_admin' ? `<button data-action="open-delete-role" data-id="${esc(r.code)}" class="px-3 py-1 rounded-lg bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 font-bold">حذف الدور</button>` : '<span class="text-slate-400 text-xs">دور محمي</span>'}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }



  // ============================================================================
  // Main App Shell, Router, Modals, Full CRUD & Section 32 Complete Journey
  // ============================================================================

  function renderCurrentPageContent() {
    const navObj = NAV_ITEMS.find(n => n.id === state.page) || NAV_ITEMS[0];
    if (!hasAccess(navObj.perm)) {
      return `
        <div class="surface-card bg-white rounded-2xl border-2 border-red-300 p-8 text-center max-w-xl mx-auto my-12 space-y-3">
          <div class="text-4xl">🔒</div>
          <h2 class="text-xl font-black text-red-700">وصول مقيد بموجب صلاحيات النظام (RBAC Access Denied)</h2>
          <p class="text-xs text-slate-600 leading-relaxed">
            الدور النشط حالياً هو <b>${esc(state.currentRole)}</b>، ولا يملك صلاحية الوصول إلى قسم «<b>${esc(navObj.ar)}</b>».
            هذا المستخدم غير مخوّل بفتح القسم. لتغيير الحساب، سجّل الخروج ثم ادخل بحساب مصرح له.
          </p>
          <div class="pt-3 flex justify-center gap-2">
            ${state.currentRole === 'client' ? `<button data-nav="portal" class="px-4 py-2 rounded-xl bg-navy text-white text-xs font-bold">الانتقال إلى بوابة الباحث</button>` : ''}
          </div>
        </div>
      `;
    }

    switch (state.page) {
      case 'dashboard': return renderDashboard();
      case 'inbox': return renderInbox();
      case 'contacts': return renderContacts();
      case 'leads': return renderLeadsTable();
      case 'pipeline': return renderPipelineKanban();
      case 'catalog': return renderCatalog();
      case 'pricing': return renderPricingEngine();
      case 'quotes': return renderQuotes();
      case 'contracts': return renderContracts();
      case 'projects': return renderProjectsERP();
      case 'tasks': return renderTasks();
      case 'timeline': return renderTimelineSchedule();
      case 'team': return renderTeam();
      case 'invoices': return renderInvoices();
      case 'payments': return renderPaymentsAndInstallments();
      case 'reports': return renderReportsBI();
      case 'ai_center': return renderAIAgentCenter();
      case 'knowledge': return renderKnowledgeBase();
      case 'automation': return renderAutomation();
      case 'integrations': return renderIntegrations();
      case 'portal': return renderClientPortal();
      case 'files': return renderFilesDMS();
      case 'notifications': return renderNotifications();
      case 'approvals': return renderApprovals();
      case 'audit': return renderAuditLogs();
      case 'settings': return renderSettingsModule();
      case 'rbac': return renderUsersRBAC();
      default: return renderDashboard();
    }
  }

  function renderAppShell() {
    if (!state.authenticated) {
      return renderLoginScreen();
    }

    const activeNav = NAV_ITEMS.find(n => n.id === state.page) || NAV_ITEMS[0];
    const unreadInb = db.conversations.reduce((a, c) => a + (Number(c.unread_count) || 0), 0);
    const pendingAppCount = db.approvals.filter(a => a.status === 'قيد الانتظار').length;
    const unreadNotifCount = db.notifications.filter(n => !n.is_read).length;

    const groups = [...new Set(NAV_ITEMS.map(i => i.group))];

    return `
      <!-- Desktop App Window Frame Header -->
      <div class="desktop-titlebar px-4 flex items-center justify-between text-white text-[11px] no-print">
        <div class="flex items-center gap-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-red-400"></span>
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-400"></span>
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          <span class="font-bold mr-2">UES SMART ERP — Desktop Application (v2.5.2 Security Update)</span>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-teal-soft font-semibold">● SQLite / Server Engine Active (45 Tables)</span>
          <span class="ltr-num text-slate-300">2026-11-10</span>
        </div>
      </div>

      <div class="flex-1 flex min-h-0">
        <!-- Collapsible Sidebar (All 27 Sections) -->
        <aside class="${state.sidebarCollapsed ? 'w-20' : 'w-68'} bg-navy text-white flex-shrink-0 flex flex-col border-l border-white/10 select-none no-print transition-all">
          <div class="p-4 border-b border-white/10 flex items-center justify-between gap-2">
            <div class="flex items-center gap-2.5 overflow-hidden">
              <div class="w-10 h-10 rounded-xl bg-teal text-white flex items-center justify-center font-black text-base flex-shrink-0 shadow">UES</div>
              ${!state.sidebarCollapsed ? `
                <div class="truncate">
                  <div class="font-extrabold text-xs leading-tight">المتحدة للخدمات التعليمية</div>
                  <div class="text-[10px] text-teal-soft truncate">United Educational Services</div>
                </div>
              ` : ''}
            </div>
            <button data-action="toggle-sidebar" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs" title="طي/توسيع القائمة">⇄</button>
          </div>

          <nav class="flex-1 overflow-y-auto sidebar-scroll p-2.5 space-y-3">
            ${groups.map(grp => `
              <div>
                ${!state.sidebarCollapsed ? `<div class="px-2.5 py-1 text-[10px] font-extrabold text-slate-400 uppercase">${esc(grp)}</div>` : ''}
                <div class="space-y-0.5">
                  ${NAV_ITEMS.filter(item => item.group === grp).map(item => {
                    const isActive = state.page === item.id;
                    const badgeVal = item.id === 'inbox' ? unreadInb : item.id === 'approvals' ? pendingAppCount : item.id === 'notifications' ? unreadNotifCount : 0;
                    return `
                      <button data-nav="${esc(item.id)}" class="w-full flex items-center justify-between gap-2 px-3 py-2 rounded-xl text-xs transition ${isActive ? 'bg-teal text-white font-extrabold shadow' : 'text-slate-300 hover:bg-white/10 hover:text-white'}">
                        <div class="flex items-center gap-2.5 truncate">
                          <span class="text-sm">${item.icon}</span>
                          ${!state.sidebarCollapsed ? `<span class="truncate">${item.num}. ${esc(state.lang === 'en' ? item.en : item.ar)}</span>` : ''}
                        </div>
                        ${!state.sidebarCollapsed && badgeVal > 0 ? `<span class="px-1.5 py-0.2 rounded-full bg-amber-500 text-navy font-black text-[10px] ltr-num">${badgeVal}</span>` : ''}
                      </button>
                    `;
                  }).join('')}
                </div>
              </div>
            `).join('')}
          </nav>

          <div class="p-3 border-t border-white/10 bg-navy-dark/60 text-xs flex items-center justify-between">
            ${!state.sidebarCollapsed ? `
              <div class="truncate">
                <div class="font-bold text-white truncate">${esc(state.currentProfile ? state.currentProfile.full_name : state.currentUser.email)}</div>
                <div class="text-[10px] text-teal-soft ltr-num">${esc(state.currentUser.username || state.currentUser.email)} • ${esc(state.currentRole)}</div>
              </div>
            ` : ''}
            <button data-action="change-my-password" class="px-2.5 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-[11px] font-bold" title="تغيير كلمة المرور">🔑 تغيير كلمة المرور</button>
            <button data-action="logout" class="px-2.5 py-1.5 rounded-lg bg-red-600/80 hover:bg-red-600 text-white text-[11px] font-bold" title="تسجيل الخروج">خروج</button>
          </div>
        </aside>

        <!-- Main Content Area -->
        <div class="flex-1 flex flex-col min-w-0">
          <!-- Sticky Top Navigation Bar -->
          <header class="surface-card bg-white border-b border-bordercol px-5 py-3 sticky top-0 z-30 flex flex-wrap items-center justify-between gap-3 no-print">
            <div class="flex items-center gap-3">
              <div>
                <div class="text-[11px] text-mutedtxt font-semibold">UES SMART ERP / ${esc(activeNav.group)}</div>
                <div class="text-base font-black text-navy">${activeNav.num}. ${esc(state.lang === 'en' ? activeNav.en : activeNav.ar)}</div>
              </div>
            </div>

            <div class="flex flex-wrap items-center gap-2.5">
              <input type="search" id="global-search-input" value="${esc(state.searchQuery)}" placeholder="بحث سريع (عميل، عرض، مشروع)..." class="px-3 py-1.5 rounded-xl border border-bordercol text-xs w-48 sm:w-60" />

              <span class="text-[11px] font-bold text-teal" title="الدور ثابت حسب حساب تسجيل الدخول">🔒 ${esc(ROLE_MATRIX[state.currentRole]?.label || state.currentRole)}</span>

              <button data-action="toggle-lang" class="px-2.5 py-1.5 rounded-xl border border-bordercol text-xs font-bold hover:bg-slate-100 ltr-num">
                ${state.lang === 'ar' ? 'EN / LTR' : 'عربي / RTL'}
              </button>

              <button data-action="toggle-dark" class="px-2.5 py-1.5 rounded-xl border border-bordercol text-xs font-bold hover:bg-slate-100">
                ${state.darkMode ? '☀️ نهاري' : '🌙 ليلي'}
              </button>

              <button data-nav="notifications" class="relative px-2.5 py-1.5 rounded-xl border border-bordercol text-xs font-bold hover:bg-slate-100">
                🔔 ${unreadNotifCount > 0 ? `<span class="text-amber-600 font-black ltr-num">(${unreadNotifCount})</span>` : ''}
              </button>
            </div>
          </header>

          <main class="flex-1 p-5 max-w-[1600px] w-full mx-auto">
            ${renderCurrentPageContent()}
          </main>

          <footer class="px-6 py-3 border-t border-bordercol text-center text-[11px] text-mutedtxt no-print flex flex-wrap items-center justify-between gap-2">
            <span>المتحدة للخدمات التعليمية (United Educational Services) — UES SMART ERP</span>
            <span>حالة الذكاء الاصطناعي: ${state.aiApiKeyConnected ? 'مفتاح OpenAI (gpt-4o) مهيأ بأمان في الخادم (غير متصل — محاكاة محلية)' : 'غير متصل — وضع تجريبي'} • الأسعار مصنفة DEMO</span>
          </footer>
        </div>
      </div>
    `;
  }

  function renderApp() {
    const htmlRoot = document.getElementById('html-root');
    if (htmlRoot) {
      htmlRoot.setAttribute('dir', state.lang === 'en' ? 'ltr' : 'rtl');
      htmlRoot.setAttribute('lang', state.lang);
      if (state.darkMode) htmlRoot.classList.add('dark');
      else htmlRoot.classList.remove('dark');
    }
    const root = document.getElementById('app-root');
    if (root) root.innerHTML = renderAppShell();
    if (typeof scheduleDesktopSave === 'function') scheduleDesktopSave();
  }

  // ============================================================================
  // SECTION 32 — COMPLETE 19-STEP FUNCTIONAL USER JOURNEY (AUTOMATED E2E FLOW)
  // ============================================================================
  function executeCompleteUserJourney() {
    const jSuffix = String(db.contacts.length + 101);
    const contactId = `C-${jSuffix}`;
    const convId = `CONV-${jSuffix}`;
    const leadId = `LD-${jSuffix}`;
    const quoteId = `QT-${jSuffix}`;
    const quoteNum = `QT-2026-${jSuffix}`;
    const contractId = `CT-${jSuffix}`;
    const contractNum = `CNT-2026-${jSuffix}`;
    const projectId = `PRJ-${jSuffix}`;
    const projectCode = `PRJ-2026-${jSuffix}`;
    const invId = `INV-${jSuffix}`;
    const invNum = `INV-2026-${jSuffix}`;
    const payId = `PAY-${jSuffix}`;
    const payRef = `VERIFIED-JOURNEY-REF-${jSuffix}`;
    const ts = nowStr();

    // Steps 1, 2, 3: Receive message, create Conversation & Contact
    const newContact = {
      id: contactId,
      organization_id: state.currentUser.organization_id,
      full_name: `د. طارق الزهراني (رحلة باحث #${jSuffix})`,
      phone: `+96655000${jSuffix}`,
      email: `tarek.${jSuffix}@researcher.example.com`,
      country: 'السعودية',
      city: 'جدة',
      university: 'جامعة الملك عبد العزيز',
      faculty: 'كلية الاقتصاد والإدارة',
      academic_degree: 'دكتوراه',
      research_field: 'إدارة الأعمال والتحول الاستراتيجي',
      preferred_language: 'ar',
      preferred_channel: 'Website Live Chat',
      source: 'Website Live Chat',
      priority: 'عالية',
      customer_status: 'نشط',
      lifetime_value_cents: 617310,
      assigned_sales_id: 'U-SR',
      marketing_consent: 1,
      ai_processing_consent: 1,
      tags_json: '["دكتوراه","استشارة منهجية","تحليل بيانات"]',
      notes: 'سيناريو القسم 32 المتكامل: استشارة منهجية وتحليل بيانات دكتوراه.',
      merged_into_id: null,
      is_archived: 0,
      created_at: ts,
      updated_at: ts,
      created_by: 'SYSTEM-JOURNEY'
    };
    db.contacts.unshift(newContact);

    db.conversations.unshift({
      id: convId,
      organization_id: state.currentUser.organization_id,
      contact_id: contactId,
      channel_id: 'CH-WEB',
      channel_name: 'Website Live Chat',
      status: 'مفتوحة',
      priority: 'عالية',
      unread_count: 0,
      assigned_to: 'U-SR',
      handling_mode: 'Human',
      tags_json: '["رحلة كاملة"]',
      handoff_history_json: JSON.stringify([{ at: ts, from: 'AI', to: 'أ. كريم عادل', reason: 'تأهيل الباحث وإعداد عرض سعر' }]),
      last_message_text: 'السلام عليكم، عندي بحث دكتوراه وأحتاج استشارة منهجية وتحليل بيانات.',
      last_message_at: ts,
      created_at: ts,
      updated_at: ts
    });

    db.messages.push(
      { id: uid('MSG'), organization_id: state.currentUser.organization_id, conversation_id: convId, sender_type: 'customer', sender_name: newContact.full_name, body: 'السلام عليكم، عندي بحث دكتوراه وأحتاج استشارة منهجية وتحليل بيانات.', message_type: 'text', related_entity_id: null, created_at: ts },
      { id: uid('MSG'), organization_id: state.currentUser.organization_id, conversation_id: convId, sender_type: 'ai', sender_name: 'UES Academic Business Assistant', body: 'وعليكم السلام د. طارق. تم تسجيل متطلبات بحث الدكتوراه (استشارة منهجية + تحليل إحصائي) وحساب العرض المبدئي وإحالته للاعتماد.', message_type: 'text', related_entity_id: quoteId, created_at: ts }
    );

    // Steps 4 & 5: Record requirements & create Lead
    db.leads.unshift({
      id: leadId,
      organization_id: state.currentUser.organization_id,
      contact_id: contactId,
      service_id: 'SVC-06',
      title: `استشارة منهجية وتحليل بيانات دكتوراه — ${newContact.full_name}`,
      stage: 'مكتسب',
      lost_reason: null,
      estimated_value_cents: 617310,
      currency: 'EGP',
      lead_score: 95,
      priority: 'عالية',
      assigned_to: 'U-SR',
      last_contact_at: ts.slice(0, 10),
      next_followup_at: '2026-11-15',
      target_delivery_date: '2026-11-26',
      notes: 'متطلبات الباحث: منهجية دكتوراه + تحليل SmartPLS',
      created_at: ts,
      updated_at: ts
    });

    // Steps 6, 7, 8, 9, 10: Select service, calculate quote, save, approve, record acceptance
    const calc = computePricing('SVC-06', 1, 'متقدم', 'عادي', 'دكتوراه', 5, 14, 'EGP');
    db.quotes.unshift({
      id: quoteId,
      organization_id: state.currentUser.organization_id,
      quote_number: quoteNum,
      contact_id: contactId,
      lead_id: leadId,
      service_id: 'SVC-06',
      title: 'استشارة منهجية وتحليل إحصائي للبيانات الفعلية',
      description: 'رحلة الباحث الكاملة (القسم 32) — يشمل فحص المنهجية وتحليل البيانات.',
      pricing_method: 'Price per Statistical Analysis',
      quantity: 1,
      unit_price_cents: calc.baseCents,
      complexity_level: 'متقدم',
      complexity_multiplier: calc.compM,
      urgency_level: 'عادي',
      urgency_multiplier: calc.urgM,
      academic_level: 'دكتوراه',
      academic_multiplier: calc.acadM,
      discount_pct: 5,
      discount_cents: calc.discCents,
      tax_pct: 14,
      tax_cents: calc.taxCents,
      total_cents: calc.totalEgpCents,
      estimated_cost_cents: calc.estCostCents,
      currency: 'EGP',
      proposed_duration_days: 12,
      delivery_terms: 'تسليم مرحلي معتمد',
      revision_policy: 'مراجعتان مجانيتان خلال 14 يوماً',
      payment_terms: '30% تعاقد - 30% مرحلة أولى - 30% مرحلة ثانية - 10% تسليم نهائي',
      valid_until: '2026-11-25',
      status: 'مقبول',
      created_at: ts,
      updated_at: ts
    });

    db.approvals.unshift({
      id: `APR-${jSuffix}`,
      organization_id: state.currentUser.organization_id,
      request_type: 'اعتماد عرض سعر رحلة الباحث',
      related_entity_id: quoteId,
      requester_name: 'أ. كريم عادل',
      client_name: newContact.full_name,
      amount_display: fmtMoneyPlain(calc.totalEgpCents, 'EGP'),
      reason: 'اعتماد عرض رحلة الباحث الكاملة (القسم 32)',
      assigned_approver: 'د. طارق المنشاوي',
      status: 'معتمد',
      decided_by: 'د. طارق المنشاوي',
      decision_notes: 'معتمد للتنفيذ الفوري',
      requested_at: ts,
      decided_at: ts
    });

    // Steps 11 & 12: Create Contract & 30/30/30/10 Installment Schedule
    db.contracts.unshift({
      id: contractId,
      organization_id: state.currentUser.organization_id,
      contract_number: contractNum,
      contact_id: contactId,
      quote_id: quoteId,
      title: `عقد استشارة منهجية وتحليل بيانات — ${newContact.full_name}`,
      contract_value_cents: calc.totalEgpCents,
      currency: 'EGP',
      scope_of_work: 'تنفيذ استشارة المنهجية والتحليل الإحصائي SmartPLS.',
      deliverables: 'تقرير المنهجية + نتائج التحليل المفسرة',
      start_date: '2026-11-10',
      agreed_deadline: '2026-11-26',
      installments_json: '[30,30,30,10]',
      revision_terms: 'مراجعتان مجانيتان خلال 14 يوماً',
      confidentiality_terms: 'سرية تامة لبيانات الباحث',
      cancellation_terms: 'احتساب المراحل المنجزة فقط',
      template_lang: 'ar',
      approval_status: 'معتمد',
      signature_status: 'موافقة مسجلة (محاكاة)',
      signed_at: '2026-11-10',
      created_at: ts,
      updated_at: ts
    });

    [30, 30, 30, 10].forEach((pct, idx) => {
      db.contract_milestones.push({
        id: `MS-${contractId}-${idx + 1}`,
        organization_id: state.currentUser.organization_id,
        contract_id: contractId,
        milestone_order: idx + 1,
        title: `القسط ${idx + 1} (${pct}%) — ${contractNum}`,
        percentage: pct,
        amount_cents: Math.round(calc.totalEgpCents * (pct / 100)),
        due_date: '2026-11-20',
        status: idx === 0 ? 'محصلة' : 'مجدولة',
        created_at: ts
      });
    });

    // Steps 13, 14, 15: Create Project, Create Tasks & Assign to Staff
    db.projects.unshift({
      id: projectId,
      organization_id: state.currentUser.organization_id,
      project_code: projectCode,
      title: `مشروع بحث الدكتوراه — ${newContact.full_name}`,
      contact_id: contactId,
      contract_id: contractId,
      manager_id: 'U-AOM',
      academic_department: 'الإحصاء وتحليل البيانات',
      assigned_team_json: '["U-AOM","U-AS1","U-AS2"]',
      start_date: '2026-11-10',
      deadline: '2026-11-26',
      current_stage: 'قيد التنفيذ',
      progress_pct: 50,
      budget_cents: calc.totalEgpCents,
      internal_cost_cents: calc.estCostCents,
      currency: 'EGP',
      priority: 'عالية',
      client_notes: 'تم إطلاق المشروع فور اعتماد العقد.',
      internal_notes: 'موزع على د. علي النجار ود. منى الشافعي.',
      created_at: ts,
      updated_at: ts
    });

    db.tasks.unshift(
      {
        id: `TSK-${jSuffix}-A`,
        organization_id: state.currentUser.organization_id,
        task_code: `TSK-2026-${jSuffix}-A`,
        project_id: projectId,
        title: 'مراجعة الإطار المنهجي وفحص أداة الدراسة',
        description: 'مهمة مسندة ضمن رحلة الباحث الكاملة',
        assigned_to: 'U-AOM',
        start_date: '2026-11-10',
        due_date: '2026-11-15',
        priority: 'عالية',
        status: 'مكتملة',
        progress_pct: 100,
        estimated_hours: 6,
        actual_hours: 6,
        review_status: 'معتمدة',
        checklist_json: '[]',
        created_at: ts,
        updated_at: ts
      },
      {
        id: `TSK-${jSuffix}-B`,
        organization_id: state.currentUser.organization_id,
        task_code: `TSK-2026-${jSuffix}-B`,
        project_id: projectId,
        title: 'إجراء التحليل الإحصائي SmartPLS وتفسير الجداول',
        description: 'تحليل البيانات الفعلية للباحث',
        assigned_to: 'U-AS1',
        start_date: '2026-11-12',
        due_date: '2026-11-22',
        priority: 'عالية',
        status: 'قيد التنفيذ',
        progress_pct: 40,
        estimated_hours: 12,
        actual_hours: 5,
        review_status: 'قيد العمل',
        checklist_json: '[]',
        created_at: ts,
        updated_at: ts
      }
    );

    // Steps 16 & 17: Create Invoice & Record Verified First Installment Payment (30%) by Finance Officer
    const firstInstallmentCents = Math.round(calc.totalEgpCents * 0.30);
    db.invoices.unshift({
      id: invId,
      organization_id: state.currentUser.organization_id,
      invoice_number: invNum,
      contact_id: contactId,
      contract_id: contractId,
      milestone_title: `دفعة التعاقد الأولى (30%) — ${contractNum}`,
      amount_cents: firstInstallmentCents,
      tax_cents: Math.round(firstInstallmentCents * 0.14),
      paid_cents: firstInstallmentCents,
      remaining_cents: 0,
      currency: 'EGP',
      due_date: '2026-11-12',
      status: 'مدفوعة',
      created_at: ts,
      updated_at: ts
    });

    db.payments.unshift({
      id: payId,
      organization_id: state.currentUser.organization_id,
      payment_number: `PAY-2026-${jSuffix}`,
      invoice_id: invId,
      contact_id: contactId,
      amount_cents: firstInstallmentCents,
      currency: 'EGP',
      payment_method: 'Bank Transfer',
      reference_number: payRef,
      proof_document: `bank_receipt_${jSuffix}.pdf`,
      verification_source: 'finance_officer',
      verified_by: 'أ. ندى محمود (مديرة المالية)',
      paid_at: ts,
      created_at: ts
    });

    // Steps 18 & 19: Update Reports/Dashboard & Record Immutable Audit Log
    addAuditLog(
      'رحلة الباحث الكاملة (القسم 32)',
      `تنفيذ المسار المتكامل (19 خطوة): رسالة الباحث ← عميل (${contactId}) ← فرصة (${leadId}) ← عرض (${quoteNum}) ← عقد (${contractNum}) ← مشروع (${projectCode}) ← فاتورة (${invNum}) ← دفعة مؤكدة (${payRef})`,
      'journey',
      projectId
    );

    renderApp();
    openModal(
      'تم تنفيذ سيناريو رحلة الباحث الكاملة بنجاح (19 خطوة مترابطة — القسم 32)',
      `
        <div class="space-y-3 text-xs">
          <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 font-bold">
            ✅ تم تنفيذ جميع الخطوات الـ 19 وربطها بالسجلات الفعلية وتحديث لوحة التحكم والتقارير وسجل التدقيق:
          </div>
          <div class="grid sm:grid-cols-2 gap-2.5">
            <div class="p-2.5 rounded-lg bg-slate-50 border"><b>1-3. المحادثة والعميل:</b> ${esc(newContact.full_name)} (<span class="ltr-num">${esc(contactId)}</span>)</div>
            <div class="p-2.5 rounded-lg bg-slate-50 border"><b>4-5. الفرصة البيعية:</b> <span class="ltr-num">${esc(leadId)}</span> (حالة: مكتسب)</div>
            <div class="p-2.5 rounded-lg bg-slate-50 border"><b>6-10. عرض السعر المعتمد والمقبول:</b> <span class="ltr-num">${esc(quoteNum)}</span> (${fmtMoney(calc.totalEgpCents)})</div>
            <div class="p-2.5 rounded-lg bg-slate-50 border"><b>11-12. العقد وجدول الأقساط (30/30/30/10):</b> <span class="ltr-num">${esc(contractNum)}</span></div>
            <div class="p-2.5 rounded-lg bg-slate-50 border"><b>13-15. المشروع والمهام المسندة:</b> <span class="ltr-num">${esc(projectCode)}</span></div>
            <div class="p-2.5 rounded-lg bg-slate-50 border"><b>16-19. الفاتورة والدفعة المؤكدة مالياً:</b> <span class="ltr-num">${esc(invNum)}</span> (${fmtMoney(firstInstallmentCents)})</div>
          </div>
        </div>
      `,
      '',
      true
    );
  }


  // ============================================================================
  // Interactive Modals, Forms, Exports & Global Event Delegation
  // ============================================================================

  function exportEntityCSV(entity) {
    const rows = db[entity] || [];
    if (!rows.length) return showToast('لا توجد سجلات للتصدير', 'warning');
    const keys = Object.keys(rows[0]);
    const csvLines = [
      keys.join(','),
      ...rows.map(r => keys.map(k => `"${String(r[k] ?? '').replace(/"/g, '""')}"`).join(','))
    ];
    const blob = new Blob(['\ufeff' + csvLines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `UES_SMART_ERP_${entity}_2026.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
    addAuditLog('تصدير تقارير', `تصدير ملف CSV لقسم ${entity}`);
    showToast(`تم تصدير ملف CSV (${entity}) بنجاح`);
  }

  function exportFullDatabaseJSON() {
    const blob = new Blob([JSON.stringify({ system: 'UES-SMART-ERP', exportedAt: nowStr(), database: db }, null, 2)], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'UES_SMART_ERP_FULL_BACKUP_2026.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
    addAuditLog('نسخ احتياطي', 'تصدير نسخة احتياطية كاملة لقاعدة البيانات JSON');
    showToast('تم تصدير النسخة الاحتياطية الكاملة بنجاح');
  }

  function evaluateAIScenarioInput(promptText) {
    const q = promptText.trim();
    const modeLabel = state.aiApiKeyConnected ? 'متصل — OpenAI API (gpt-4o عبر الخادم)' : 'غير متصل — وضع تجريبي';
    let intent = 'new_researcher_qualification';
    let tool = 'lookup_service() + create_lead()';
    let toolOut = 'تأهيل باحث جديد وربط الخدمة من الكتالوج.';
    let reply = `[${modeLabel}] وعليكم السلام ورحمة الله، أهلاً بحضرتك في المتحدة للخدمات التعليمية (UES). يسعدنا مساعدتك في بحث الدكتوراه؛ يرجى تزويدنا بالجامعة والتخصص الدقيق وحجم الملف المتوفر والموعد النهائي لإعداد عرض السعر المعتمد.`;
    let risk = 'منخفض';

    if (/اختلاق|فبركة|تزوير|وهمية|غير موجودة|ضمان قبول/i.test(q)) {
      intent = 'academic_integrity_violation_refusal';
      tool = 'get_company_policy(policy="academic_integrity")';
      toolOut = 'ميثاق النزاهة الأكاديمية KB-01: رفض قاطع لاختلاق النتائج أو المراجع.';
      reply = `[${modeLabel}] نعتذر، تلتزم المتحدة للخدمات التعليمية (UES) بميثاق النزاهة الأكاديمية الصارم؛ نرفض اختلاق نتائج استبيان أو فبركة مراجع غير موجودة. يسعدنا تقديم دعم علمي مشروع في تحليل بياناتك الفعلية وتوثيق المراجع الحقيقية.`;
      risk = 'مرتفع — حماية نزاهة أكاديمية';
    } else if (/خصم\s*(1[1-9]|[2-9][0-9])|خصم 20|خصم ٢٠/i.test(q)) {
      intent = 'discount_exceeds_limit';
      tool = 'request_manager_approval(discount_pct=20, max_limit=10)';
      toolOut = 'تم رفع طلب موافقة خصم استثنائي للإدارة.';
      reply = `[${modeLabel}] الحد الأقصى للخصم المباشر المسموح به هو 10%. نظراً لأن الخصم المطلوب (20%) يتجاوز السقف المعتمد، قمت برفع طلب موافقة للإدارة عبر request_manager_approval() وسنوافيك بالرد فور اعتماده.`;
      risk = 'متوسط — يتطلب موافقة مدير';
    } else if (/يومين|خلال يومين|مستعجل|بكرة/i.test(q)) {
      intent = 'urgent_request_capacity_check';
      tool = 'check_team_capacity(department="Academic & Stats", days=2)';
      toolOut = 'فحص السعة الحقيقية للفريق قبل الوعد بموعد تسليم.';
      reply = `[${modeLabel}] قمت بفحص جدول الفريق عبر check_team_capacity(). لا نعد بالتسليم خلال يومين قبل فحص حجم الملف والتأكد من توفر أخصائي متفرغ؛ يرجى إرسال الملف لتأكيد إمكانية التنفيذ العاجل.`;
      risk = 'متوسط — فحص سعة';
    } else if (/حولت|دفعت|الدفعة|إيصال|انستاباي|instapay/i.test(q)) {
      intent = 'payment_verification_request';
      tool = 'get_invoice_status() + create_followup_task(dept="Finance")';
      toolOut = 'تسجيل طلب تحقق مالي لدى قسم الحسابات.';
      reply = `[${modeLabel}] شكراً لك. يرجى إرسال رقم العملية المرجعي ومستند الإثبات؛ تم تسجيل طلب تحقق للمالية، علماً أن تأكيد الدفع لا يتم آلياً عبر الذكاء الاصطناعي بل يتطلب اعتماد الموظف المالي المختص.`;
      risk = 'متوسط — تحقق مالي';
    } else if (/اتأخر|شكوى|المدير|مشكلة/i.test(q)) {
      intent = 'complaint_human_escalation';
      tool = 'handoff_to_human(priority="urgent", reason="complaint")';
      toolOut = 'تم تسجيل شكوى وتحويل المحادثة لمسؤول بشري.';
      reply = `[${modeLabel}] نعتذر عن أي تأخير. قمت بتسجيل شكوى عاجلة وتحويل المحادثة فوراً إلى المسؤول المختص عبر handoff_to_human() للتواصل معك مباشرة.`;
      risk = 'مرتفع — تصعيد بشري';
    } else if (/بكام|سعر|تكلفة|إحصائي|احصائي/i.test(q)) {
      intent = 'price_inquiry';
      tool = 'lookup_service(code="UES-STA-301") + calculate_quote()';
      toolOut = 'استرجاع السعر الأساسي لخدمة التحليل الإحصائي (3,800 EGP DEMO).';
      reply = `[${modeLabel}] خدمة التحليل الإحصائي (SPSS / AMOS / SmartPLS) متاحة بسعر أساسي استرشادي 3,800 EGP (DEMO). لتحديد السعر النهائي نحتاج معرفة حجم العينة وعدد المتغيرات والفروض وموعد التسليم.`;
      risk = 'منخفض';
    }

    db.ai_conversation_runs.unshift({
      id: uid('AIRUN'),
      organization_id: state.currentUser.organization_id,
      scenario_code: state.aiSelectedScenario,
      user_input: q,
      detected_intent: intent,
      invoked_tool: tool,
      tool_output_summary: toolOut,
      ai_response: reply,
      risk_level: risk,
      requires_human_approval: risk !== 'منخفض' ? 1 : 0,
      mode_label: modeLabel,
      created_at: nowStr()
    });
    db.agents[0].token_usage_count += 340;
    addAuditLog('مركز الذكاء الاصطناعي', `تشغيل سيناريو AI (${intent}) واستدعاء ${tool}`);
    return reply;
  }

  // Global Click Handler
  document.addEventListener('click', async function(e) {
    const navBtn = e.target.closest('[data-nav]');
    if (navBtn) {
      e.preventDefault();
      const target = navBtn.getAttribute('data-nav');
      const destination = NAV_ITEMS.find(n => n.id === target);
      if (!state.authenticated || !destination || !hasAccess(destination.perm)) {
        showToast('ليس لديك صلاحية الوصول إلى هذا القسم', 'error');
        return;
      }
      state.page = target;
      closeModal();
      renderApp();
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    const actBtn = e.target.closest('[data-action]');
    if (!actBtn) {
      if (e.target.id === 'modal-backdrop') closeModal();
      return;
    }

    const action = actBtn.getAttribute('data-action');
    const id = actBtn.getAttribute('data-id') || '';

    switch (action) {
      case 'close-modal':
        closeModal();
        break;
      case 'toggle-sidebar':
        state.sidebarCollapsed = !state.sidebarCollapsed;
        renderApp();
        break;
      case 'toggle-dark':
        state.darkMode = !state.darkMode;
        renderApp();
        break;
      case 'toggle-lang':
        state.lang = state.lang === 'ar' ? 'en' : 'ar';
        renderApp();
        break;
      case 'logout':
        await fetch('/api/auth/logout', {method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).catch(()=>{});
        state.authenticated = false;
        state.currentRole = '';
        state.currentUser = null;
        state.currentProfile = null;
        desktopPersistenceReady = false;
        state.loginUsername = '';
        state.loginPassword = '';
        db = emptyDatabase();
        state.loginError = '';
        renderApp();
        showToast('تم تسجيل الخروج من الجلسة بأمان');
        break;
      case 'switch-login-portal': {
        const pKey = actBtn.getAttribute('data-portal') || 'owner';
        state.loginPortalTab = pKey;
        state.loginUsername = '';
        state.loginPassword = '';
        state.loginError = '';
        renderApp();
        break;
      }
      case 'forgot-password':
        showToast('استعادة كلمة المرور غير متصلة بخدمة بريد في النسخة المحلية التجريبية', 'warning');
        break;
      case 'test-unauthorized-signup':
        state.loginError = 'مرفوض أمنياً (Section 5 RBAC): لا يُسمح لأي مستخدم عام بإنشاء مؤسسة بديلة أو منح نفسه صلاحية المالك بمجرد التسجيل.';
        renderApp();
        showToast('تم منع محاولة إنشاء مؤسسة بديلة بنجاح', 'error');
        break;
      case 'run-full-journey':
        executeCompleteUserJourney();
        break;
      case 'select-conv':
        state.selectedConvId = id;
        const cv = db.conversations.find(x => x.id === id);
        if (cv) cv.unread_count = 0;
        renderApp();
        break;
      case 'open-conv-direct':
        state.selectedConvId = id;
        state.page = 'inbox';
        renderApp();
        break;
      case 'toggle-conv-ai': {
        const c = db.conversations.find(x => x.id === id);
        if (c) {
          c.handling_mode = c.handling_mode === 'AI' ? 'Human' : 'AI';
          const hist = JSON.parse(c.handoff_history_json || '[]');
          hist.unshift({ at: nowStr(), from: c.handling_mode === 'AI' ? 'موظف' : 'AI', to: c.handling_mode, reason: 'تبديل يدوي من شريط المحادثة' });
          c.handoff_history_json = JSON.stringify(hist);
          addAuditLog('صندوق الرسائل', `تغيير وضع المحادثة ${id} إلى ${c.handling_mode}`);
          renderApp();
          showToast(`تم تغيير وضع المحادثة إلى ${c.handling_mode}`);
        }
        break;
      }
      case 'insert-saved-reply': {
        const box = document.getElementById('inbox-message-input');
        if (box) {
          box.value = actBtn.getAttribute('data-text') || '';
          box.focus();
        }
        break;
      }
      case 'ai-draft-inbox': {
        const c = db.conversations.find(x => x.id === id);
        const lastMsg = db.messages.filter(m => m.conversation_id === id && m.sender_type === 'customer').slice(-1)[0];
        const reply = evaluateAIScenarioInput(lastMsg ? lastMsg.body : 'السلام عليكم');
        const box = document.getElementById('inbox-message-input');
        if (box) box.value = reply;
        showToast('تم توليد مسودة رد ذكي من قاعدة المعرفة المعتمدة');
        break;
      }
      case 'send-quote-in-chat': {
        const c = db.conversations.find(x => x.id === id);
        if (c) {
          db.messages.push({
            id: uid('MSG'),
            organization_id: state.currentUser.organization_id,
            conversation_id: c.id,
            sender_type: 'staff',
            sender_name: state.currentProfile ? state.currentProfile.full_name : 'المبيعات',
            body: '📄 تم إرفاق عرض السعر المعتمد للمراجعة والقبول.',
            message_type: 'quote_card',
            related_entity_id: 'QT-101',
            created_at: nowStr()
          });
          c.last_message_text = '📄 تم إرفاق عرض السعر المعتمد';
          c.last_message_at = nowStr();
          renderApp();
          showToast('تم إرفاق عرض السعر في المحادثة');
        }
        break;
      }
      case 'simulate-inbound-msg': {
        const newCid = uid('C');
        const newCname = `باحث زائر جديد (${db.contacts.length + 1})`;
        db.contacts.unshift({
          id: newCid, organization_id: state.currentUser.organization_id, full_name: newCname,
          phone: '+201066554433', email: 'new.researcher@example.com', country: 'مصر', city: 'القاهرة',
          university: 'جامعة عين شمس', faculty: 'كلية التجارة', academic_degree: 'دكتوراه',
          research_field: 'المحاسبة والمراجعة', preferred_language: 'ar', preferred_channel: 'Website Live Chat',
          source: 'Website Live Chat', priority: 'عالية', customer_status: 'نشط', lifetime_value_cents: 0,
          assigned_sales_id: 'U-SR', marketing_consent: 1, ai_processing_consent: 1, tags_json: '["جديد"]',
          notes: 'رسالة واردة جديدة', created_at: nowStr(), updated_at: nowStr()
        });
        const newConvId = uid('CONV');
        db.conversations.unshift({
          id: newConvId, organization_id: state.currentUser.organization_id, contact_id: newCid, channel_id: 'CH-WEB',
          channel_name: 'Website Live Chat', status: 'مفتوحة', priority: 'عالية', unread_count: 1,
          assigned_to: 'U-SR', handling_mode: 'AI', tags_json: '["وارد جديد"]', handoff_history_json: '[]',
          last_message_text: 'السلام عليكم، محتاج مساعدة في خطة دكتوراه وتحليل إحصائي.', last_message_at: nowStr(),
          created_at: nowStr(), updated_at: nowStr()
        });
        db.messages.push({
          id: uid('MSG'), organization_id: state.currentUser.organization_id, conversation_id: newConvId,
          sender_type: 'customer', sender_name: newCname,
          body: 'السلام عليكم، محتاج مساعدة في خطة دكتوراه وتحليل إحصائي.', message_type: 'text', created_at: nowStr()
        });
        state.selectedConvId = newConvId;
        renderApp();
        showToast('تم استقبال رسالة باحث جديد وتوجيهها للصندوق الموحد');
        break;
      }
      case 'review-identity-merge': {
        const pending = db.contact_identities.filter(i => i.merge_review_status === 'pending_review');
        openModal('مراجعة حالات دمج الهويات المشتركة (Identity Merge Protection)', `
          <div class="space-y-3 text-xs">
            <div class="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900">
              قواعد الأمان (القسم 7 و8): يمنع النظام دمج حسابات أشخاص مختلفين تلقائياً لمجرد تشابه الأسماء، ويشترط مراجعة بشرية لتأكيد الهوية.
            </div>
            ${pending.map(p => `
              <div class="p-3.5 rounded-xl border border-slate-200 flex items-center justify-between">
                <div>
                  <div class="font-bold text-navy">حساب خارجي: <span class="ltr-num">${esc(p.external_identifier)}</span> (${esc(p.channel_type)})</div>
                  <div class="text-mutedtxt">مرتبط مبدئياً بـ: ${esc(getContactName(p.contact_id))}</div>
                </div>
                <span class="px-2 py-1 rounded bg-amber-100 text-amber-900 font-bold">محجوز للمراجعة البشرية</span>
              </div>
            `).join('') || '<div class="text-mutedtxt">لا توجد حالات دمج معلقة</div>'}
          </div>
        `);
        break;
      }
      case 'handoff-conv-modal': {
        openModal('تحويل المحادثة إلى موظف مختص', `
          <input type="hidden" name="conv_id" value="${esc(id)}" />
          <div class="space-y-3 text-xs">
            <div>
              <label class="block font-bold mb-1">اختر الموظف المستقبل:</label>
              <select name="assigned_to" class="w-full p-2.5 rounded-xl border border-slate-300 font-bold">
                ${db.profiles.map(p => `<option value="${esc(p.user_id)}">${esc(p.full_name)} (${esc(p.department)})</option>`).join('')}
              </select>
            </div>
            <div>
              <label class="block font-bold mb-1">سبب التحويل:</label>
              <input type="text" name="reason" value="متابعة متطلبات فنية وعرض سعر" required class="w-full p-2.5 rounded-xl border border-slate-300" />
            </div>
          </div>
        `, 'submit-handoff-conv');
        break;
      }
      case 'open-contact-modal': {
        const c = db.contacts.find(x => x.id === id) || {};
        openModal(c.id ? 'تعديل ملف باحث' : 'إضافة باحث / عميل جديد', `
          <input type="hidden" name="id" value="${esc(c.id || '')}" />
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div><label class="block font-bold mb-1">الاسم الكامل *</label><input name="full_name" value="${esc(c.full_name || '')}" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">رقم الهاتف الدولي *</label><input name="phone" value="${esc(c.phone || '+2010')}" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">البريد الإلكتروني</label><input type="email" name="email" value="${esc(c.email || '')}" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">الدولة *</label><input name="country" value="${esc(c.country || 'مصر')}" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">الجامعة / المؤسسة</label><input name="university" value="${esc(c.university || '')}" class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">الدرجة العلمية</label>
              <select name="academic_degree" class="w-full p-2.5 rounded-xl border font-bold">
                ${['دكتوراه','ماجستير','بكالوريوس','باحث مستقل'].map(d => `<option value="${d}" ${c.academic_degree===d?'selected':''}>${d}</option>`).join('')}
              </select>
            </div>
            <div class="sm:col-span-2"><label class="block font-bold mb-1">التخصص الأكاديمي الدقيق</label><input name="research_field" value="${esc(c.research_field || '')}" class="w-full p-2.5 rounded-xl border" /></div>
            <div class="sm:col-span-2"><label class="block font-bold mb-1">ملاحظات داخلية</label><textarea name="notes" rows="2" class="w-full p-2.5 rounded-xl border">${esc(c.notes || '')}</textarea></div>
          </div>
        `, 'save-contact');
        break;
      }
      case 'view-contact-360': {
        const c = db.contacts.find(x => x.id === id);
        if (!c) break;
        openModal(`ملف الباحث الشامل 360° — ${c.full_name}`, `
          <div class="space-y-3 text-xs">
            <div class="grid sm:grid-cols-2 gap-2.5 p-3.5 rounded-xl bg-slate-50 border">
              <div><b>الجامعة:</b> ${esc(c.university || '—')}</div>
              <div><b>التخصص:</b> ${esc(c.research_field || '—')}</div>
              <div><b>الهاتف:</b> <span class="ltr-num">${esc(c.phone)}</span></div>
              <div><b>البريد:</b> <span class="ltr-num">${esc(c.email)}</span></div>
              <div><b>قيمة التعاملات LTV:</b> ${fmtMoney(c.lifetime_value_cents)}</div>
              <div><b>موافقة معالجة AI:</b> ${c.ai_processing_consent ? 'موافق ✓' : 'غير مفعل'}</div>
            </div>
            <div class="p-3 rounded-xl border"><b>الملاحظات:</b> ${esc(c.notes || 'لا توجد')}</div>
          </div>
        `);
        break;
      }
      case 'open-lead-modal': {
        openModal('إضافة فرصة بيعية جديدة (New Sales Lead)', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div class="sm:col-span-2"><label class="block font-bold mb-1">عنوان الفرصة *</label><input name="title" required placeholder="مثال: استشارة منهجية وتحليل إحصائي دكتوراه" class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">الباحث</label>
              <select name="contact_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.contacts.map(c => `<option value="${esc(c.id)}">${esc(c.full_name)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">الخدمة المطلوبة</label>
              <select name="service_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.services.map(s => `<option value="${esc(s.id)}">${esc(s.name_ar)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">القيمة التقديرية (EGP)</label><input type="number" name="estimated_egp" value="3800" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">موعد التسليم المستهدف</label><input type="date" name="target_delivery_date" value="2026-11-25" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
          </div>
        `, 'save-lead');
        break;
      }
      case 'advance-lead-stage': {
        const l = db.leads.find(x => x.id === id);
        if (l) {
          const idx = PIPELINE_STAGES.indexOf(l.stage);
          const nextIdx = (idx + 1) % (PIPELINE_STAGES.length - 1); // cycles up to 'مكتسب'
          l.stage = PIPELINE_STAGES[nextIdx];
          addAuditLog('مسار المبيعات', `نقل الفرصة ${l.id} إلى مرحلة (${l.stage})`);
          renderApp();
          showToast(`تم نقل الفرصة إلى مرحلة: ${l.stage}`);
        }
        break;
      }
      case 'quote-from-lead': {
        const l = db.leads.find(x => x.id === id);
        if (l) {
          state.calcContactId = l.contact_id;
          state.calcServiceId = l.service_id || 'SVC-06';
          state.page = 'pricing';
          renderApp();
          showToast('تم تحميل بيانات الفرصة في محرك التسعير الذكي');
        }
        break;
      }
      case 'create-quote-from-conv': {
        state.calcContactId = id;
        state.page = 'pricing';
        renderApp();
        break;
      }
      case 'price-this-service': {
        state.calcServiceId = id;
        state.page = 'pricing';
        renderApp();
        break;
      }
      case 'open-service-modal': {
        openModal('إضافة خدمة جديدة إلى الكتالوج الأكاديمي (DEMO Pricing)', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div><label class="block font-bold mb-1">كود الخدمة *</label><input name="service_code" value="UES-NEW-${db.services.length+101}" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">التصنيف</label>
              <select name="category_name_ar" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.service_categories.map(c => `<option value="${esc(c.name_ar)}">${esc(c.name_ar)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">اسم الخدمة بالعربية *</label><input name="name_ar" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">اسم الخدمة بالإنجليزية *</label><input name="name_en" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">السعر الأساسي التجريبي (EGP - DEMO) *</label><input type="number" name="base_egp" value="2500" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">المدة الدنيا (أيام)</label><input type="number" name="min_duration_days" value="7" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div class="sm:col-span-2"><label class="block font-bold mb-1">وصف الخدمة والمخرجات</label><textarea name="description" rows="2" required class="w-full p-2.5 rounded-xl border"></textarea></div>
          </div>
        `, 'save-service');
        break;
      }
      case 'create-quote-from-calculator': {
        const calc = computePricing(state.calcServiceId, state.calcQty, state.calcComplexity, state.calcUrgency, state.calcAcademic, state.calcDiscountPct, state.calcTaxPct, state.calcCurrency);
        const qId = uid('QT');
        const qNum = `QT-2026-${db.quotes.length + 101}`;
        const st = calc.requiresApproval ? 'بانتظار الاعتماد' : 'مسودة';
        db.quotes.unshift({
          id: qId, organization_id: state.currentUser.organization_id, quote_number: qNum,
          contact_id: state.calcContactId, lead_id: null, service_id: state.calcServiceId,
          title: calc.svc.name_ar, description: `عرض مسعر عبر محرك التسعير (${state.calcComplexity} / ${state.calcUrgency})`,
          pricing_method: calc.svc.pricing_method, quantity: calc.quantity, unit_price_cents: calc.baseCents,
          complexity_level: state.calcComplexity, complexity_multiplier: calc.compM,
          urgency_level: state.calcUrgency, urgency_multiplier: calc.urgM,
          academic_level: state.calcAcademic, academic_multiplier: calc.acadM,
          discount_pct: calc.dPct, discount_cents: calc.discCents, tax_pct: calc.tPct, tax_cents: calc.taxCents,
          total_cents: calc.convertedCents, estimated_cost_cents: calc.estCostCents, currency: state.calcCurrency,
          proposed_duration_days: calc.svc.min_duration_days, delivery_terms: 'تسليم مرحلي معتمد',
          revision_policy: calc.svc.revision_policy, payment_terms: '30% تعاقد - 30% مرحلة أولى - 30% مرحلة ثانية - 10% تسليم نهائي',
          valid_until: '2026-11-30', status: st, created_at: nowStr(), updated_at: nowStr()
        });
        if (calc.requiresApproval) {
          db.approvals.unshift({
            id: uid('APR'), organization_id: state.currentUser.organization_id, request_type: `خصم استثنائي (${calc.dPct}%)`,
            related_entity_id: qId, requester_name: state.currentProfile ? state.currentProfile.full_name : 'المبيعات',
            client_name: getContactName(state.calcContactId), amount_display: fmtMoneyPlain(calc.convertedCents, state.calcCurrency),
            reason: `الخصم المطلوب (${calc.dPct}%) يتجاوز السقف التلقائي (${calc.maxLimit}%)`,
            assigned_approver: 'د. طارق المنشاوي', status: 'قيد الانتظار', requested_at: nowStr()
          });
        }
        addAuditLog('عروض الأسعار', `إصدار عرض السعر ${qNum} بحالة (${st})`);
        state.page = 'quotes';
        renderApp();
        showToast(calc.requiresApproval ? `تم حفظ العرض ${qNum} وإحالته لموافقة المدير لتجاوز سقف الخصم` : `تم إنشاء عرض السعر ${qNum} بنجاح`);
        break;
      }
      case 'preview-quote-pdf': {
        const q = db.quotes.find(x => x.id === id);
        if (!q) break;
        openModal(`معاينة وثيقة عرض السعر الثنائية اللغة — ${q.quote_number}`, `
          <div class="p-5 rounded-2xl border-2 border-navy space-y-4 text-xs bg-white">
            <div class="flex items-center justify-between border-b pb-3">
              <div>
                <div class="text-base font-black text-navy">المتحدة للخدمات التعليمية | United Educational Services</div>
                <div class="text-[11px] text-mutedtxt">Official Academic Quotation • عرض سعر رسمي (DEMO)</div>
              </div>
              <div class="text-left ltr-num font-bold">${esc(q.quote_number)}<br/>Valid Until: ${esc(q.valid_until)}</div>
            </div>
            <div class="grid grid-cols-2 gap-3 bg-slate-50 p-3 rounded-xl">
              <div><b>الباحث / Researcher:</b> ${esc(getContactName(q.contact_id))}</div>
              <div><b>الحالة / Status:</b> ${esc(q.status)}</div>
              <div><b>الخدمة / Service:</b> ${esc(q.title)}</div>
              <div><b>شروط الدفع / Payment:</b> 30% / 30% / 30% / 10%</div>
            </div>
            <div class="flex justify-between items-center p-4 rounded-xl bg-navy text-white">
              <span class="font-bold">الإجمالي النهائي المعتمد (Total Amount):</span>
              <span class="text-xl font-black text-teal-soft">${fmtMoney(q.total_cents, q.currency)}</span>
            </div>
            <div class="flex justify-end">
              <button type="button" onclick="window.print()" class="px-4 py-2 rounded-xl bg-teal text-white font-bold">🖨️ طباعة / حفظ PDF</button>
            </div>
          </div>
        `, '', true);
        break;
      }
      case 'quote-next-status': {
        const q = db.quotes.find(x => x.id === id);
        const nextSt = actBtn.getAttribute('data-next');
        if (q && nextSt) {
          q.status = nextSt;
          addAuditLog('عروض الأسعار', `تحديث حالة العرض ${q.quote_number} إلى ${nextSt}`);
          renderApp();
          showToast(`تم تحديث حالة العرض إلى: ${nextSt}`);
        }
        break;
      }
      case 'approve-quote-btn': {
        if (!canMutate('approvals')) return showToast('غير مصرح لهذا الدور باعتماد العروض', 'error');
        const q = db.quotes.find(x => x.id === id);
        if (q) {
          q.status = 'معتمد';
          const ap = db.approvals.find(a => a.related_entity_id === q.id);
          if (ap) {
            ap.status = 'معتمد';
            ap.decided_by = state.currentProfile ? state.currentProfile.full_name : 'الإدارة';
            ap.decided_at = nowStr();
          }
          addAuditLog('الموافقات', `اعتماد عرض السعر ${q.quote_number}`);
          renderApp();
          showToast(`تم اعتماد العرض ${q.quote_number} بنجاح`);
        }
        break;
      }
      case 'open-contract-from-quote':
      case 'open-new-contract-modal': {
        const acceptedQuotes = db.quotes.filter(q => q.status === 'مقبول');
        const selQ = db.quotes.find(q => q.id === id) || acceptedQuotes[0];
        if (!selQ) return showToast('يرجى قبول عرض سعر أولاً قبل إنشاء العقد', 'warning');
        openModal('إعداد عقد اتفاق أكاديمي وجدول الأقساط (30/30/30/10)', `
          <div class="space-y-3 text-xs">
            <div><label class="block font-bold mb-1">عرض السعر المقبول</label>
              <select name="quote_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${acceptedQuotes.map(q => `<option value="${esc(q.id)}" ${q.id===selQ.id?'selected':''}>${esc(q.quote_number)} — ${esc(getContactName(q.contact_id))} (${fmtMoneyPlain(q.total_cents, q.currency)})</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">عنوان العقد *</label><input name="title" value="عقد اتفاق خدمات أكاديمية — ${esc(selQ.title)}" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">موعد التسليم المتفق عليه *</label><input type="date" name="agreed_deadline" value="2026-11-28" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div class="grid grid-cols-4 gap-2">
              <div><label class="block font-bold mb-1">دفعة 1 (%)</label><input type="number" name="p1" value="30" required class="w-full p-2 rounded-lg border ltr-num" /></div>
              <div><label class="block font-bold mb-1">دفعة 2 (%)</label><input type="number" name="p2" value="30" required class="w-full p-2 rounded-lg border ltr-num" /></div>
              <div><label class="block font-bold mb-1">دفعة 3 (%)</label><input type="number" name="p3" value="30" required class="w-full p-2 rounded-lg border ltr-num" /></div>
              <div><label class="block font-bold mb-1">دفعة 4 (%)</label><input type="number" name="p4" value="10" required class="w-full p-2 rounded-lg border ltr-num" /></div>
            </div>
            <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-900">يجب أن يساوي مجموع النسب 100% بالضبط.</div>
          </div>
        `, 'save-contract');
        break;
      }
      case 'view-contract-template': {
        const k = db.contracts.find(x => x.id === id);
        if (!k) break;
        openModal(`وثيقة العقد الأكاديمي (AR / EN) — ${k.contract_number}`, `
          <div class="p-5 rounded-2xl border space-y-3 text-xs leading-relaxed">
            <h3 class="text-base font-black text-navy">${esc(k.title)}</h3>
            <div><b>الطرف الأول:</b> شركة المتحدة للخدمات التعليمية (United Educational Services - UES)</div>
            <div><b>الطرف الثاني (الباحث):</b> ${esc(getContactName(k.contact_id))}</div>
            <div><b>نطاق العمل:</b> ${esc(k.scope_of_work)}</div>
            <div><b>القيمة الإجمالية:</b> ${fmtMoney(k.contract_value_cents, k.currency)} • <b>جدول الأقساط:</b> <span class="ltr-num">${esc(k.installments_json)}</span></div>
            <div><b>شروط المراجعات والسرية:</b> ${esc(k.revision_terms)} — ${esc(k.confidentiality_terms)}</div>
            <div class="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 font-bold">
              حالة التوقيع: ${esc(k.signature_status)} (لا يُعتبر الضغط الداخلي توقيعاً إلكترونياً قانونياً ملزماً إلا بعد الربط بمزود توقيع معتمد).
            </div>
          </div>
        `, '', true);
        break;
      }
      case 'convert-contract-to-project': {
        const k = db.contracts.find(x => x.id === id);
        if (!k) break;
        const pId = uid('PRJ');
        const pCode = `PRJ-2026-${db.projects.length + 101}`;
        db.projects.unshift({
          id: pId, organization_id: state.currentUser.organization_id, project_code: pCode,
          title: k.title, contact_id: k.contact_id, contract_id: k.id,
          manager_id: 'U-AOM', academic_department: 'العمليات الأكاديمية',
          assigned_team_json: '["U-AOM","U-AS1"]', start_date: k.start_date, deadline: k.agreed_deadline,
          current_stage: 'قيد التنفيذ', progress_pct: 0, budget_cents: k.contract_value_cents,
          internal_cost_cents: Math.round(k.contract_value_cents * 0.55), currency: k.currency,
          priority: 'عالية', client_notes: 'تم إنشاء المشروع من العقد المعتمد', internal_notes: '',
          created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('المشروعات', `تحويل العقد ${k.contract_number} إلى مشروع ${pCode}`);
        state.page = 'projects';
        renderApp();
        showToast(`تم إنشاء المشروع ${pCode} من العقد بنجاح`);
        break;
      }
      case 'set-project-view':
        state.projectViewMode = actBtn.getAttribute('data-mode') || 'table';
        renderApp();
        break;
      case 'advance-project-stage': {
        const p = db.projects.find(x => x.id === id);
        const stgs = ['التخطيط','قيد التنفيذ','مراجعة داخلية','جاهز للتسليم','مكتمل'];
        if (p) {
          const i = stgs.indexOf(p.current_stage);
          p.current_stage = stgs[(i + 1) % stgs.length];
          addAuditLog('المشروعات', `تحديث مرحلة المشروع ${p.project_code} إلى ${p.current_stage}`);
          renderApp();
          showToast(`تم تحديث مرحلة المشروع إلى: ${p.current_stage}`);
        }
        break;
      }
      case 'open-project-modal': {
        openModal('إضافة مشروع أكاديمي جديد', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div class="sm:col-span-2"><label class="block font-bold mb-1">عنوان المشروع *</label><input name="title" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">الباحث</label>
              <select name="contact_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.contacts.map(c => `<option value="${esc(c.id)}">${esc(c.full_name)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">القسم الأكاديمي</label><input name="academic_department" value="العمليات الأكاديمية" class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">الميزانية (EGP)</label><input type="number" name="budget_egp" value="4500" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">موعد التسليم</label><input type="date" name="deadline" value="2026-11-28" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
          </div>
        `, 'save-project');
        break;
      }
      case 'open-task-modal': {
        const preProj = actBtn.getAttribute('data-project') || db.projects[0]?.id;
        openModal('إضافة وتوزيع مهمة أكاديمية جديدة', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div class="sm:col-span-2"><label class="block font-bold mb-1">عنوان المهمة *</label><input name="title" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">المشروع</label>
              <select name="project_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.projects.map(p => `<option value="${esc(p.id)}" ${p.id===preProj?'selected':''}>${esc(p.title)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">إسناد إلى الأخصائي</label>
              <select name="assigned_to" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.profiles.map(p => `<option value="${esc(p.user_id)}">${esc(p.full_name)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">الساعات المقدرة</label><input type="number" name="estimated_hours" value="6" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div><label class="block font-bold mb-1">تاريخ الاستحقاق</label><input type="date" name="due_date" value="2026-11-20" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
          </div>
        `, 'save-task');
        break;
      }
      case 'complete-task': {
        const t = db.tasks.find(x => x.id === id);
        if (t) {
          t.status = 'مكتملة';
          t.progress_pct = 100;
          t.review_status = 'معتمدة';
          addAuditLog('المهام', `إنجاز واعتماد المهمة ${t.task_code}`);
          renderApp();
          showToast('تم اعتماد إنجاز المهمة وتحديث نسبة تقدم المشروع تلقائياً');
        }
        break;
      }
      case 'reopen-task': {
        const t = db.tasks.find(x => x.id === id);
        if (t) {
          t.status = 'قيد التنفيذ';
          t.progress_pct = 50;
          renderApp();
        }
        break;
      }
      case 'remind-task':
        showToast('تم إرسال تنبيه موعد التسليم إلى الأخصائي المكلف');
        break;
      case 'open-invoice-modal': {
        openModal('إصدار فاتورة مطالبة مالية جديدة', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div><label class="block font-bold mb-1">الباحث / العميل</label>
              <select name="contact_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.contacts.map(c => `<option value="${esc(c.id)}">${esc(c.full_name)}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">المبلغ (EGP) *</label><input type="number" name="amount_egp" value="2000" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            <div class="sm:col-span-2"><label class="block font-bold mb-1">بيان الفاتورة / القسط *</label><input name="milestone_title" value="دفعة مرحلة تنفيذ أكاديمية" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">تاريخ الاستحقاق *</label><input type="date" name="due_date" value="2026-11-22" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
          </div>
        `, 'save-invoice');
        break;
      }
      case 'open-payment-modal': {
        const preInvId = actBtn.getAttribute('data-invoice') || db.invoices.find(i => i.remaining_cents > 0)?.id || db.invoices[0]?.id;
        const inv = db.invoices.find(i => i.id === preInvId) || db.invoices[0];
        openModal('تسجيل وتأكيد دفعة مالية بموافقة المالية (Verified Payment)', `
          <div class="space-y-3 text-xs">
            <div class="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 font-semibold">
              قاعدة القسم 17: تأكيد الدفع لا يتم بواسطة الذكاء الاصطناعي وحده؛ يشترط تحقق موظف المالية ورقم مرجعي فريد لمنع التكرار (Idempotency).
            </div>
            <div><label class="block font-bold mb-1">الفاتورة</label>
              <select name="invoice_id" class="w-full p-2.5 rounded-xl border font-bold">
                ${db.invoices.map(i => `<option value="${esc(i.id)}" ${i.id===inv?.id?'selected':''}>${esc(i.invoice_number)} — ${esc(getContactName(i.contact_id))} (المتبقي: ${fmtMoneyPlain(i.remaining_cents, i.currency)})</option>`).join('')}
              </select>
            </div>
            <div class="grid sm:grid-cols-2 gap-3">
              <div><label class="block font-bold mb-1">المبلغ المحصل (EGP) *</label><input type="number" step="0.01" name="amount_egp" value="${((inv?.remaining_cents || 100000)/100).toFixed(2)}" required class="w-full p-2.5 rounded-xl border ltr-num font-bold" /></div>
              <div><label class="block font-bold mb-1">طريقة الدفع المعتمدة</label>
                <select name="payment_method" class="w-full p-2.5 rounded-xl border font-bold">
                  ${['InstaPay','Bank Transfer','Vodafone Cash','Payment Gateway','Cash'].map(m => `<option value="${m}">${m}</option>`).join('')}
                </select>
              </div>
              <div><label class="block font-bold mb-1">رقم العملية المرجعي الفريد (Unique Reference) *</label><input name="reference_number" value="REF-2026-${Math.floor(100000 + Math.random()*900000)}" required class="w-full p-2.5 rounded-xl border ltr-num font-mono" /></div>
              <div><label class="block font-bold mb-1">مستند الإثبات المرفق</label><input name="proof_document" value="verified_receipt_scan.pdf" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            </div>
          </div>
        `, 'save-payment');
        break;
      }
      case 'open-expense-modal': {
        openModal('تسجيل مصروف تشغيلي جديد', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div class="sm:col-span-2"><label class="block font-bold mb-1">بيان المصروف *</label><input name="title" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">التصنيف</label><input name="category" value="تكاليف تشغيل أكاديمي" class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">المبلغ (EGP) *</label><input type="number" name="amount_egp" value="500" required class="w-full p-2.5 rounded-xl border ltr-num" /></div>
          </div>
        `, 'save-expense');
        break;
      }
      case 'select-ai-scenario': {
        const k = actBtn.getAttribute('data-key') || 'A';
        state.aiSelectedScenario = k;
        state.aiCustomPrompt = AI_SCENARIOS[k].text;
        renderApp();
        break;
      }
      case 'toggle-ai-system':
        db.agents[0].system_enabled = db.agents[0].system_enabled ? 0 : 1;
        renderApp();
        showToast(db.agents[0].system_enabled ? 'تم تفعيل وكيل AI على مستوى النظام' : 'تم إيقاف وكيل AI مؤقتاً');
        break;
      case 'toggle-ai-key-sim':
        state.aiApiKeyConnected = false;
        if (db.agents && db.agents[0]) db.agents[0].connection_mode = 'غير متصل — محاكاة فقط';
        showToast('الذكاء الاصطناعي في هذه النسخة محاكاة محلية وليس اتصال API حقيقياً', 'warning');
        renderApp();
        break;
      case 'open-kb-modal': {
        openModal('رفع وتوثيق مستند جديد في قاعدة المعرفة (RAG Knowledge Document)', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div class="sm:col-span-2"><label class="block font-bold mb-1">عنوان السياسة / المستند *</label><input name="title" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">التصنيف</label><input name="category" value="السياسات المعتمدة" class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">نوع الملف</label>
              <select name="file_type" class="w-full p-2.5 rounded-xl border font-bold ltr-num">
                ${['PDF','DOCX','TXT','CSV','XLSX'].map(t => `<option value="${t}">${t}</option>`).join('')}
              </select>
            </div>
            <div class="sm:col-span-2"><label class="block font-bold mb-1">النص المستخرج والمعتمد للوكيل *</label><textarea name="extracted_text" rows="3" required class="w-full p-2.5 rounded-xl border"></textarea></div>
          </div>
        `, 'save-kb-doc');
        break;
      }
      case 'toggle-kb-approval': {
        const doc = db.knowledge_documents.find(d => d.id === id);
        if (doc && !doc.is_client_uploaded) {
          doc.approval_status = doc.approval_status === 'معتمد' ? 'مسودة' : 'معتمد';
          renderApp();
          showToast(`تم تحديث حالة المستند إلى: ${doc.approval_status}`);
        } else {
          showToast('لا يمكن اعتماد مرفق عميل غير موثق كسياسة للوكيل', 'error');
        }
        break;
      }
      case 'toggle-automation': {
        const r = db.automation_rules.find(x => x.id === id);
        if (r) {
          r.is_enabled = r.is_enabled ? 0 : 1;
          renderApp();
        }
        break;
      }
      case 'run-all-automations': {
        db.automation_rules.filter(r => r.is_enabled).forEach(r => { r.run_count += 1; });
        addAuditLog('الأتمتة', 'تشغيل دورة فحص قواعد الأتمتة بنجاح مع ضمان عدم تكرار السجلات (Idempotency)');
        renderApp();
        showToast('تم تنفيذ دورة فحص قواعد الأتمتة المفعلة بنجاح');
        break;
      }
      case 'open-automation-modal': {
        openModal('إضافة قاعدة أتمتة جديدة (Automation Builder)', `
          <div class="space-y-3 text-xs">
            <div><label class="block font-bold mb-1">اسم القاعدة *</label><input name="title" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">الحدث المشغل (Trigger)</label>
              <select name="trigger_event" class="w-full p-2.5 rounded-xl border ltr-num font-bold">
                ${['New Message Received','New Lead Created','Quotation Approved','Contract Approved','Payment Verified','Task Overdue','Invoice Overdue'].map(t => `<option value="${t}">${t}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">الإجراء المطلوب (Action) *</label><input name="action_type" value="Notify Manager & Create Follow-up Task" required class="w-full p-2.5 rounded-xl border" /></div>
          </div>
        `, 'save-automation');
        break;
      }
      case 'test-channel-conn': {
        const ch = db.channels.find(x => x.id === id);
        if (ch) {
          if (ch.connection_status === 'connected') {
            showToast(`القناة ${ch.name} متصلة وتعمل بنجاح في بيئة المحاكاة`);
          } else {
            showToast(`القناة ${ch.name} غير متصلة: بانتظار إدخال مفاتيح API الرسمية في الخادم (لا يدعي النظام اتصالاً وهمياً)`, 'warning');
          }
        }
        break;
      }
      case 'config-channel-modal': {
        const ch = db.channels.find(x => x.id === id);
        if (!ch) break;
        openModal(`إعدادات الربط الرسمي — ${ch.name}`, `
          <div class="space-y-3 text-xs">
            <div class="p-3 rounded-xl bg-slate-50 border">
              <b>واجهة API الرسمية:</b> <span class="ltr-num">${esc(ch.api_type)}</span><br/>
              <b>الحالة الحالية:</b> ${esc(ch.connection_status)}<br/>
              <b>القيود:</b> ${esc(ch.limitations_note)}
            </div>
            <div class="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900">
              يتم تخزين الرموز السرية (Tokens / Secrets) في متغيرات البيئة الخادمية (.env) ولا تُعرض في المتصفح.
            </div>
          </div>
        `);
        break;
      }
      case 'download-signed-file':
      case 'preview-file': {
        const f = db.files.find(x => x.id === id);
        if (f) {
          const token = Math.random().toString(36).substring(2, 12);
          openModal(`معاينة آمنة ورابط تحميل موقّت — ${f.file_name}`, `
            <div class="space-y-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 border space-y-1">
                <div><b>التصنيف:</b> ${esc(f.category)} • <b>الإصدار:</b> ${esc(f.version_label)}</div>
                <div><b>مستوى الصلاحية:</b> ${esc(f.access_level)}</div>
                <div><b>ملخص المحتوى:</b> ${esc(f.content_preview || '')}</div>
              </div>
              <div class="p-3 rounded-xl bg-navy text-teal-soft font-mono text-[11px] ltr-num break-all">
                Signed URL (Expires in 15m): https://storage.ues-erp.local/v1/files/${esc(f.id)}?sig=${token}&exp=900
              </div>
            </div>
          `);
        }
        break;
      }
      case 'open-file-modal': {
        openModal('رفع مستند جديد إلى نظام إدارة الملفات (DMS)', `
          <div class="grid sm:grid-cols-2 gap-3 text-xs">
            <div class="sm:col-span-2"><label class="block font-bold mb-1">اسم الملف *</label><input name="file_name" placeholder="مثال: تقرير_التحليل_الإحصائي_النهائي.pdf" required class="w-full p-2.5 rounded-xl border" /></div>
            <div><label class="block font-bold mb-1">التصنيف</label>
              <select name="category" class="w-full p-2.5 rounded-xl border font-bold ltr-num">
                ${['Research Documents','Questionnaires','Statistical Data','Contracts','Invoices','Deliverables','Reviewer Comments','Revision Files','Internal Documents'].map(c => `<option value="${c}">${c}</option>`).join('')}
              </select>
            </div>
            <div><label class="block font-bold mb-1">مستوى الصلاحية</label>
              <select name="access_level" class="w-full p-2.5 rounded-xl border font-bold">
                <option value="فريق المشروع والباحث">فريق المشروع والباحث</option>
                <option value="داخلي سري">داخلي سري (محجوب عن الباحث)</option>
              </select>
            </div>
          </div>
        `, 'save-file');
        break;
      }
      case 'mark-all-notifs-read':
        db.notifications.forEach(n => { n.is_read = 1; });
        renderApp();
        showToast('تم تحديد جميع الإشعارات كمقروءة');
        break;
      case 'quick-approve':
      case 'quick-reject': {
        if (!canMutate('approvals')) return showToast('غير مصرح لهذا الدور بالبت في الموافقات الإدارية', 'error');
        const ap = db.approvals.find(x => x.id === id);
        if (ap) {
          ap.status = action === 'quick-approve' ? 'معتمد' : 'مرفوض';
          ap.decided_by = state.currentProfile ? state.currentProfile.full_name : state.currentUser.email;
          ap.decided_at = nowStr();
          const q = db.quotes.find(x => x.id === ap.related_entity_id);
          if (q) q.status = ap.status;
          addAuditLog('الموافقات الإدارية', `قرار (${ap.status}) على الطلب ${ap.id} بواسطة ${ap.decided_by}`);
          renderApp();
          showToast(`تم تسجيل القرار (${ap.status}) وتوثيق اسم المعتمد والتوقيت`);
        }
        break;
      }
      case 'set-settings-tab':
        state.settingsTab = actBtn.getAttribute('data-tab') || 'Company Profile';
        renderApp();
        break;
      case 'change-my-password': {
        if (!state.authenticated) break;
        openModal('تغيير كلمة مرور حسابي', `<div class="space-y-3 text-sm">
          <label class="block font-bold">كلمة المرور الحالية</label><input type="password" name="old_password" required autocomplete="current-password" class="p-3 rounded-xl border w-full ltr-num" />
          <label class="block font-bold">كلمة المرور الجديدة (12 حرفًا على الأقل)</label><input type="password" name="new_password" required minlength="12" autocomplete="new-password" class="p-3 rounded-xl border w-full ltr-num" />
          <p class="text-xs text-slate-600">لا تظهر كلمات المرور في قوائم المستخدمين ولا يمكن لأي مسؤول قراءتها بعد الحفظ.</p>
        </div>`, 'save-change-my-password');
        break;
      }
      case 'open-delete-role': {
        if (!state.authenticated || state.currentRole !== 'super_admin' || !state.currentUser?.is_owner) return showToast('حذف الأدوار متاح للمالك فقط','error');
        if (id === 'super_admin') return showToast('لا يمكن حذف دور المالك','error');
        const role = db.roles.find(r => r.code === id);
        if (!role) return showToast('الدور غير موجود','error');
        const count = db.users.filter(u=>u.role_code===id).length;
        openModal(`حذف الدور: ${role.name_ar}`, `
          <div class="space-y-4 text-sm">
            <div class="p-3 bg-red-50 border border-red-200 rounded-xl">سيتم حذف الدور من النظام. ${count ? `هناك ${count} حساب مرتبط به، لذلك يجب نقلهم إلى دور آخر قبل الحذف.` : 'هذا الدور غير مرتبط بأي حساب حاليًا.'}</div>
            <input type="hidden" name="role_code" value="${esc(id)}" />
            ${count ? `<label class="block font-bold">إعادة إسناد المستخدمين إلى دور آخر</label><select required name="replacement_role" class="w-full p-3 border rounded-xl">${db.roles.filter(r=>r.code!==id && r.code!=='super_admin').map(r=>`<option value="${esc(r.code)}">${esc(r.name_ar)}</option>`).join('')}</select>` : '<input type="hidden" name="replacement_role" value="" />'}
            <label class="flex items-center gap-2"><input name="confirm" type="checkbox" required /> أفهم أن هذا الإجراء سيحذف الدور ويغير صلاحيات المستخدمين المرتبطين به.</label>
          </div>`, 'delete-role-confirm');
        break;
      }
      case 'change-staff-role': {
        if(state.currentRole!=='super_admin'||!state.currentUser?.is_owner) return showToast('للمالك فقط','error');
        const target=db.users.find(u=>u.id===id);
        if(!target||target.is_owner) return showToast('لا يمكن تعديل دور مالك النظام','error');
        openModal('تعديل دور الموظف — المالك فقط',`<div class="space-y-3 text-sm">
          <input type="hidden" name="user_id" value="${esc(target.id)}" />
          <label class="font-bold block">اختيار الدور الجديد</label>
          <select name="role_code" class="w-full p-3 border rounded-xl">${db.roles.filter(r=>r.code!=='super_admin').map(r=>`<option value="${esc(r.code)}" ${r.code===target.role_code?'selected':''}>${esc(r.name_ar)}</option>`).join('')}</select>
          <p class="text-red-700">سيتم إنهاء جلسات الموظف الحالية، وسيحتاج إلى تسجيل الدخول من جديد.</p>
        </div>`,'save-staff-role');
        break;
      }
      case 'activate-staff': {
        if(state.currentRole!=='super_admin'||!state.currentUser?.is_owner) return showToast('للمالك فقط','error');
        if(!confirm('تفعيل الحساب مع إصدار كلمة مرور جديدة مؤقتة؟')) break;
        try {
          const resp=await fetch('/api/admin/users/activate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:id})});
          const payload=await resp.json();if(!resp.ok||!payload.ok) throw new Error(payload.error||'فشل التفعيل');
          await refreshCentralState(true);
          openModal('كلمة مرور مؤقتة — مرة واحدة فقط',`<div class="space-y-3"><p>تُسلّم للموظف عبر قناة آمنة، ويجب عليه تغييرها بعد الدخول.</p><div class="p-3 bg-slate-100 font-mono select-all ltr-num break-all">${esc(payload.temporary_password)}</div></div>`);
        } catch(err){showToast(err.message,'error')}
        break;
      }
      case 'reset-user-password': {
        if (state.currentRole !== 'super_admin' || !state.currentUser?.is_owner) return showToast('إعادة تعيين كلمات المرور للمالك فقط','error');
        const target = db.users.find(u=>u.id===id);
        if (!target || !confirm(`إعادة تعيين كلمة مرور حساب ${target.username}؟ سيتم إبطال جلساته السابقة.`)) break;
        try {
          const resp=await fetch('/api/admin/users/reset-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:id})});
          const payload=await resp.json();
          if(!resp.ok || !payload.ok) throw new Error(payload.error || 'فشل إعادة التعيين');
          openModal('كلمة مرور مؤقتة — تُعرض مرة واحدة للمالك', `<div class="space-y-3"><p class="font-bold text-red-700">انسخ كلمة المرور المؤقتة وأرسلها للمستخدم عبر قناة آمنة. لا يمكن استرجاع كلمة المرور السابقة.</p><div class="p-3 rounded-xl bg-slate-100 font-mono ltr-num select-all break-all">${esc(payload.temporary_password)}</div><p class="text-xs text-slate-600">تظهر هذه الكلمة هنا لمرة واحدة فقط. لا تسجلها في ملفات عامة.</p></div>`);
          await initializeDesktopState();
        } catch(err) { showToast(err.message,'error'); }
        break;
      }
      case 'open-create-user-modal':
      case 'open-invite-modal': {
        if (state.currentRole !== 'super_admin' || !state.currentUser?.is_owner) {
          showToast('مرفوض أمنياً: إضافة حسابات للمستخدمين متاحة حصراً من خلال المالك', 'error');
          break;
        }
        openModal('إنشاء حساب مستخدم جديد وتحديد الدور والصلاحيات (بواسطة الأدمن Ahmed_99 فقط)', `
          <div class="space-y-3 text-xs">
            <div class="p-3 rounded-xl bg-teal/10 border border-teal/30 text-navy font-bold">
              🔐 بصفتك الأدمن (<b>Ahmed_99</b>)، يمكنك إنشاء حساب مخصص لأي موظف (مدير عام، مدير مبيعات، سيلز، أكاديمي، مالية، أو باحث) بيوزر وباسوورد خاصين به، وسيتم تقييد الحساب تلقائياً بصلاحيات دوره وبوابته المخصصة.
            </div>
            <div class="grid sm:grid-cols-2 gap-3">
              <div><label class="block font-bold mb-1">الاسم الكامل للموظف / المستخدم *</label><input name="full_name" placeholder="مثال: أ. محمد طارق" required class="w-full p-2.5 rounded-xl border" /></div>
              <div><label class="block font-bold mb-1">المسمى الوظيفي *</label><input name="job_title" value="مسؤول مبيعات أكاديمية" required class="w-full p-2.5 rounded-xl border" /></div>
              <div><label class="block font-bold mb-1">اسم المستخدم للدخول (Username) *</label><input name="username" placeholder="مثال: sales_mohamed" required class="w-full p-2.5 rounded-xl border ltr-num font-bold" /></div>
              <div><label class="block font-bold mb-1">كلمة المرور الخاصة به (Password) *</label><input type="password" name="password" minlength="12" autocomplete="new-password" placeholder="12 حرفًا على الأقل" required class="w-full p-2.5 rounded-xl border ltr-num font-bold" /></div>
              <div><label class="block font-bold mb-1">الدور الوظيفي والصلاحيات (RBAC Role) *</label>
                <select name="role_code" class="w-full p-2.5 rounded-xl border font-bold">
                  ${db.roles.filter(r=>r.code!=='super_admin').map(r => `<option value="${esc(r.code)}">${esc(r.name_ar)} (${esc(r.code)})</option>`).join('')}
                </select>
              </div>
              <div><label class="block font-bold mb-1">القسم التابع له *</label>
                <select name="department" class="w-full p-2.5 rounded-xl border font-bold">
                  <option value="الإدارة التنفيذية">الإدارة التنفيذية (المدير العام)</option>
                  <option value="المبيعات والتعاقدات">المبيعات والتعاقدات (المبيعات والسيلز)</option>
                  <option value="العمليات الأكاديمية">العمليات الأكاديمية</option>
                  <option value="الإحصاء وتحليل البيانات">الإحصاء وتحليل البيانات</option>
                  <option value="الإدارة المالية">الإدارة المالية</option>
                  <option value="خدمة الباحثين">خدمة الباحثين</option>
                  <option value="بوابة الباحثين">بوابة الباحثين</option>
                </select>
              </div>
              <div class="sm:col-span-2"><label class="block font-bold mb-1">البريد المؤسسي (مطلوب لإنشاء الحساب)</label><input type="email" name="email" required placeholder="user@ues-edu.com" class="w-full p-2.5 rounded-xl border ltr-num" /></div>
            </div>
          </div>
        `, 'save-new-user-account');
        break;
      }
      case 'export-csv':
        exportEntityCSV(actBtn.getAttribute('data-entity') || 'contacts');
        break;
      case 'export-db-json':
        exportFullDatabaseJSON();
        break;
    }
  });

  // Global Form Submit Handler
  document.addEventListener('submit', async function(e) {
    const form = e.target;

    if (form.id === 'login-form') {
      e.preventDefault();
      const fd = new FormData(form);
      const ident = String(fd.get('username') || '').trim();
      const pw = String(fd.get('password') || '');
      state.loginPassword='';
      try {
        const resp=await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:ident,password:pw})});
        const result=await resp.json();
        if(!resp.ok || !result.ok) throw new Error('اسم المستخدم أو كلمة المرور غير صحيحة.');
        state.authenticated = true;
        state.currentUser = result.user;
        state.currentRole = result.user.role_code;
        state.currentProfile = {user_id:result.user.id,full_name:result.user.full_name,department:result.user.department};
        state.page = result.user.role_code === 'client' ? 'portal' : 'dashboard';
        state.loginError = '';
        await initializeDesktopState();
        showToast(`مرحباً بك، ${result.user.full_name || result.user.username}`);
      } catch(err) {
        state.authenticated = false;
        state.currentRole = '';
        state.loginError = 'اسم المستخدم أو كلمة المرور غير صحيحة.';
        renderApp();
      }
      return;
    }

    if (form.id === 'inbox-send-form') {
      e.preventDefault();
      const convId = form.getAttribute('data-conv');
      const box = document.getElementById('inbox-message-input');
      const txt = box ? box.value.trim() : '';
      if (!txt) return showToast('يرجى كتابة نص الرسالة أولاً', 'warning');
      const modeInput = form.querySelector('input[name="reply_mode"]:checked');
      const rMode = modeInput ? modeInput.value : 'staff';
      const cv = db.conversations.find(x => x.id === convId);
      if (cv) {
        db.messages.push({
          id: uid('MSG'),
          organization_id: state.currentUser.organization_id,
          conversation_id: cv.id,
          sender_type: rMode,
          sender_name: state.currentProfile ? state.currentProfile.full_name : 'فريق الدعم',
          body: txt,
          message_type: 'text',
          created_at: nowStr()
        });
        if (rMode !== 'internal_note') {
          cv.last_message_text = txt;
          cv.last_message_at = nowStr();
        }
        addAuditLog('صندوق الرسائل', `إضافة ${rMode === 'internal_note' ? 'ملاحظة داخلية' : 'رد'} في المحادثة ${cv.id}`);
        renderApp();
        showToast(rMode === 'internal_note' ? 'تم حفظ الملاحظة الداخلية للفريق' : 'تم تسجيل وإرسال الرد في المحادثة');
      }
      return;
    }

    if (form.id === 'ai-playground-form') {
      e.preventDefault();
      const box = document.getElementById('ai-prompt-input');
      const txt = box ? box.value.trim() : '';
      if (!txt) return;
      state.aiCustomPrompt = txt;
      evaluateAIScenarioInput(txt);
      renderApp();
      showToast('تم تنفيذ اختبار الوكيل الذكي وتوثيق الأداة في سجل AI Audit');
      return;
    }

    if (form.id === 'settings-save-form') {
      e.preventDefault();
      const fd = new FormData(form);
      const org = db.organizations[0];
      org.name_ar = String(fd.get('name_ar') || org.name_ar);
      org.name_en = String(fd.get('name_en') || org.name_en);
      org.slogan_ar = String(fd.get('slogan_ar') || org.slogan_ar);
      org.default_currency = String(fd.get('default_currency') || org.default_currency);
      org.max_auto_discount_pct = Number(fd.get('max_auto_discount_pct') || 10);
      org.tax_rate_bps = Math.round(Number(fd.get('tax_pct') || 14) * 100);
      addAuditLog('إعدادات النظام', `تحديث إعدادات المؤسسة وسقف الخصم (${org.max_auto_discount_pct}%)`);
      renderApp();
      showToast('تم حفظ إعدادات المؤسسة وقواعد التسعير بنجاح');
      return;
    }

    if (form.id === 'dynamic-modal-form') {
      e.preventDefault();
      const subType = form.getAttribute('data-submit');
      const fd = Object.fromEntries(new FormData(form).entries());

      if (subType === 'save-change-my-password') {
        try {
          const resp=await fetch('/api/auth/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({old_password:fd.old_password,new_password:fd.new_password})});
          const result=await resp.json();
          if(!resp.ok || !result.ok) throw new Error(result.error||'فشل تغيير كلمة المرور');
          closeModal();
          showToast('تم تغيير كلمة المرور وحفظها بصورة مشفرة');
        }catch(err){showToast(err.message,'error');}
        return;
      }
      if (subType === 'save-staff-role') {
        if(!confirm('هل أنت متأكد من تغيير دور الموظف وإنهاء جلساته الحالية؟')) return;
        const resp=await fetch('/api/admin/users/set-role',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:fd.user_id,role_code:fd.role_code})});
        const payload=await resp.json();
        if(!resp.ok||!payload.ok) return showToast(payload.error||'فشل تغيير الدور','error');
        closeModal();await refreshCentralState(true);showToast('تم تغيير الدور مركزيًا وإنهاء جلسات الموظف');return;
      }
      if (subType === 'delete-role-confirm') {
        if (state.currentRole !== 'super_admin' || !state.currentUser?.is_owner) return showToast('حذف الأدوار للمالك فقط','error');
        try {
          const resp=await fetch('/api/admin/roles/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({role_code:fd.role_code,replacement_role:fd.replacement_role||''})});
          const result=await resp.json();
          if(!resp.ok || !result.ok) throw new Error(result.error||'فشل حذف الدور');
          closeModal();
          await initializeDesktopState();
          showToast(`تم حذف الدور وإعادة إسناد ${result.reassigned_users} حساب`);
        }catch(err){showToast(err.message,'error');}
        return;
      }
      if (subType === 'save-new-user-account') {
        if (state.currentRole !== 'super_admin' || !state.currentUser?.is_owner) return showToast('إنشاء الحسابات للمالك فقط','error');
        try {
          const resp=await fetch('/api/admin/users/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(fd)});
          const result=await resp.json();
          if(!resp.ok || !result.ok) throw new Error(result.error||'تعذر إنشاء الحساب');
          closeModal();
          await initializeDesktopState();
          showToast('تم إنشاء الحساب وتخزين كلمة المرور المشفرة على الخادم');
        }catch(err){showToast(err.message,'error');}
        return;
      }
      if (subType === 'submit-handoff-conv') {
        const cv = db.conversations.find(x => x.id === fd.conv_id);
        if (cv) {
          const prev = getUserName(cv.assigned_to);
          cv.assigned_to = fd.assigned_to;
          cv.handling_mode = 'Human';
          const hist = JSON.parse(cv.handoff_history_json || '[]');
          hist.unshift({ at: nowStr(), from: prev, to: getUserName(fd.assigned_to), reason: fd.reason });
          cv.handoff_history_json = JSON.stringify(hist);
          addAuditLog('صندوق الرسائل', `تحويل المحادثة ${cv.id} إلى ${getUserName(fd.assigned_to)}`);
        }
      } else if (subType === 'save-contact') {
        if (fd.id) {
          const existing = db.contacts.find(x => x.id === fd.id);
          if (existing) Object.assign(existing, fd, { updated_at: nowStr() });
        } else {
          const newId = uid('C');
          db.contacts.unshift({
            id: newId, organization_id: state.currentUser.organization_id, full_name: fd.full_name, phone: fd.phone,
            email: fd.email || '', country: fd.country, city: '', university: fd.university || '',
            faculty: '', academic_degree: fd.academic_degree, research_field: fd.research_field || '',
            preferred_language: 'ar', preferred_channel: 'WhatsApp', source: 'WhatsApp',
            priority: 'متوسطة', customer_status: 'نشط', lifetime_value_cents: 0,
            assigned_sales_id: 'U-SR', marketing_consent: 1, ai_processing_consent: 1,
            tags_json: '[]', notes: fd.notes || '', is_archived: 0, created_at: nowStr(), updated_at: nowStr()
          });
          addAuditLog('العملاء CRM', `إضافة الباحث الجديد ${fd.full_name} (${newId})`);
        }
      } else if (subType === 'save-lead') {
        const lId = uid('LD');
        db.leads.unshift({
          id: lId, organization_id: state.currentUser.organization_id, contact_id: fd.contact_id, service_id: fd.service_id,
          title: fd.title, stage: 'عميل محتمل جديد', estimated_value_cents: Math.round(Number(fd.estimated_egp || 0) * 100),
          currency: 'EGP', lead_score: 76, priority: 'عالية', assigned_to: 'U-SR',
          last_contact_at: '2026-11-10', next_followup_at: '2026-11-12', target_delivery_date: fd.target_delivery_date,
          notes: '', created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('فرص المبيعات', `إضافة فرصة بيعية جديدة ${fd.title}`);
      } else if (subType === 'save-service') {
        const sId = uid('SVC');
        db.services.unshift({
          id: sId, organization_id: state.currentUser.organization_id, service_code: fd.service_code,
          category_id: 'CAT-01', category_name_ar: fd.category_name_ar,
          name_ar: fd.name_ar, name_en: fd.name_en, description: fd.description,
          deliverables: 'مخرجات أكاديمية معتمدة', scope: 'استشارة أكاديمية',
          required_documents: 'ملف الباحث', base_price_cents: Math.round(Number(fd.base_egp || 1000) * 100),
          pricing_method: 'Fixed Price', currency: 'EGP', min_duration_days: Number(fd.min_duration_days || 7),
          estimated_hours: 14, assigned_department: 'العمليات الأكاديمية',
          revision_policy: 'مراجعتان مجانيتان خلال 14 يوماً', availability_status: 'متاحة (DEMO)',
          is_demo_price: 1, is_active: 1, created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('كتالوج الخدمات', `إضافة خدمة ${fd.name_ar} (DEMO)`);
      } else if (subType === 'save-contract') {
        const p1 = Number(fd.p1 || 0), p2 = Number(fd.p2 || 0), p3 = Number(fd.p3 || 0), p4 = Number(fd.p4 || 0);
        if (Math.abs((p1 + p2 + p3 + p4) - 100) > 0.01) {
          return showToast('خطأ: يجب أن يساوي مجموع نسب الأقساط 100% بالضبط', 'error');
        }
        const q = db.quotes.find(x => x.id === fd.quote_id);
        if (q) {
          const cId = uid('CT');
          const cNum = `CNT-2026-${db.contracts.length + 101}`;
          db.contracts.unshift({
            id: cId, organization_id: state.currentUser.organization_id, contract_number: cNum,
            contact_id: q.contact_id, quote_id: q.id, title: fd.title,
            contract_value_cents: q.total_cents, currency: q.currency,
            scope_of_work: q.description || q.title, deliverables: 'مخرجات معتمدة وفق العرض',
            start_date: '2026-11-10', agreed_deadline: fd.agreed_deadline,
            installments_json: JSON.stringify([p1, p2, p3, p4]),
            revision_terms: q.revision_policy, confidentiality_terms: 'سرية تامة لبيانات الباحث',
            cancellation_terms: 'احتساب المراحل المنجزة فقط', template_lang: 'ar',
            approval_status: 'معتمد', signature_status: 'موافقة مسجلة (محاكاة)', signed_at: '2026-11-10',
            created_at: nowStr(), updated_at: nowStr()
          });
          [p1, p2, p3, p4].forEach((pct, i) => {
            db.contract_milestones.push({
              id: `MS-${cId}-${i+1}`, organization_id: state.currentUser.organization_id, contract_id: cId,
              milestone_order: i + 1, title: `القسط ${i+1} (${pct}%)`, percentage: pct,
              amount_cents: Math.round(q.total_cents * (pct / 100)), due_date: '2026-11-22', status: 'مجدولة', created_at: nowStr()
            });
          });
          addAuditLog('العقود', `إنشاء العقد ${cNum} من العرض ${q.quote_number}`);
        }
      } else if (subType === 'save-project') {
        const pId = uid('PRJ');
        const pCode = `PRJ-2026-${db.projects.length + 101}`;
        const bud = Math.round(Number(fd.budget_egp || 4000) * 100);
        db.projects.unshift({
          id: pId, organization_id: state.currentUser.organization_id, project_code: pCode, title: fd.title,
          contact_id: fd.contact_id, contract_id: null, manager_id: 'U-AOM',
          academic_department: fd.academic_department, assigned_team_json: '["U-AOM","U-AS1"]',
          start_date: '2026-11-10', deadline: fd.deadline, current_stage: 'قيد التنفيذ',
          progress_pct: 0, budget_cents: bud, internal_cost_cents: Math.round(bud * 0.55),
          currency: 'EGP', priority: 'عالية', client_notes: '', internal_notes: '', created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('المشروعات', `إضافة المشروع ${pCode}`);
      } else if (subType === 'save-task') {
        const tId = uid('TSK');
        const tCode = `TSK-2026-${db.tasks.length + 101}`;
        db.tasks.unshift({
          id: tId, organization_id: state.currentUser.organization_id, task_code: tCode, project_id: fd.project_id,
          title: fd.title, description: '', assigned_to: fd.assigned_to, start_date: '2026-11-10',
          due_date: fd.due_date, priority: 'عالية', status: 'قيد التنفيذ', progress_pct: 25,
          estimated_hours: Number(fd.estimated_hours || 6), actual_hours: 0, review_status: 'قيد العمل',
          checklist_json: '[]', created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('المهام', `إسناد المهمة ${tCode} إلى ${getUserName(fd.assigned_to)}`);
      } else if (subType === 'save-invoice') {
        const iId = uid('INV');
        const iNum = `INV-2026-${db.invoices.length + 101}`;
        const amt = Math.round(Number(fd.amount_egp || 1000) * 100);
        db.invoices.unshift({
          id: iId, organization_id: state.currentUser.organization_id, invoice_number: iNum, contact_id: fd.contact_id,
          contract_id: null, milestone_title: fd.milestone_title, amount_cents: amt,
          tax_cents: Math.round(amt * 0.14), paid_cents: 0, remaining_cents: amt,
          currency: 'EGP', due_date: fd.due_date, status: 'صادرة', created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('الفواتير', `إصدار الفاتورة ${iNum}`);
      } else if (subType === 'save-payment') {
        const inv = db.invoices.find(i=>i.id===fd.invoice_id);
        const amtCents=Math.round(Number(fd.amount_egp||0)*100);
        if(!inv || amtCents<=0 || amtCents>inv.remaining_cents)
          return showToast('قيمة الدفعة غير صحيحة', 'error');
        const resp=await fetch('/api/finance/payments/confirm',{
          method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({invoice_id:inv.id, amount_cents:amtCents,
            payment_method:fd.payment_method,reference_number:String(fd.reference_number||'').trim(),
            proof_document:fd.proof_document||null})
        });
        const result=await resp.json().catch(()=>({}));
        if(!resp.ok||!result.ok) return showToast(result.error||'فشل اعتماد الدفعة بواسطة الخادم','error');
        closeModal();
        await refreshCentralState(true);
        showToast('تم تأكيد الدفعة في قاعدة البيانات المركزية');
        return;
      } else if (subType === 'save-expense') {
        db.expenses.unshift({
          id: uid('EXP'), organization_id: state.currentUser.organization_id, title: fd.title, category: fd.category,
          project_id: null, amount_cents: Math.round(Number(fd.amount_egp || 100) * 100),
          currency: 'EGP', expense_date: '2026-11-10', notes: '', created_at: nowStr()
        });
        addAuditLog('المصروفات', `تسجيل مصروف ${fd.title}`);
      } else if (subType === 'save-kb-doc') {
        db.knowledge_documents.unshift({
          id: uid('KB'), organization_id: state.currentUser.organization_id, title: fd.title, category: fd.category,
          source_file_name: `${fd.title.replace(/\s+/g,'_')}.${fd.file_type.toLowerCase()}`,
          file_type: fd.file_type, version_number: 'v1.0', extracted_text: fd.extracted_text,
          approval_status: 'معتمد', is_client_uploaded: 0, updated_at: nowStr(), created_at: nowStr()
        });
        addAuditLog('قاعدة المعرفة', `إضافة مستند معرفة معتمد ${fd.title}`);
      } else if (subType === 'save-automation') {
        db.automation_rules.unshift({
          id: uid('AUTO'), organization_id: state.currentUser.organization_id, title: fd.title,
          trigger_event: fd.trigger_event, condition_expr: 'شرط محقق', action_type: fd.action_type,
          responsible_user_id: 'U-OWNER', requires_approval: 0, is_enabled: 1, run_count: 1,
          last_run_at: nowStr(), created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('الأتمتة', `إضافة قاعدة أتمتة ${fd.title}`);
      } else if (subType === 'save-file') {
        db.files.unshift({
          id: uid('FIL'), organization_id: state.currentUser.organization_id, file_name: fd.file_name,
          category: fd.category, mime_type: 'application/pdf', size_kb: 540, version_label: 'v1.0',
          project_id: 'PRJ-101', contact_id: 'C-101', access_level: fd.access_level,
          is_archived: 0, signed_url_expiry_mins: 15, content_preview: 'مستند مرفوع عبر نظام DMS',
          created_at: nowStr(), updated_at: nowStr()
        });
        addAuditLog('الملفات DMS', `رفع المستند ${fd.file_name}`);
      }

      closeModal();
      renderApp();
      showToast('تم حفظ البيانات وتحديث السجلات بنجاح');
    }
  });

  // Global Change / Input Listeners for Reactive Controls
  document.addEventListener('change', function(e) {
    const t = e.target;
    if (t.getAttribute('data-action') === 'change-date-range') {
      state.dateRangeFilter = t.value;
      renderApp();
      return;
    }
    if (t.getAttribute('data-filter') === 'inbox-channel') { state.inboxChannelFilter = t.value; renderApp(); return; }
    if (t.getAttribute('data-filter') === 'inbox-status') { state.inboxStatusFilter = t.value; renderApp(); return; }
    if (t.getAttribute('data-filter') === 'inbox-mode') { state.inboxModeFilter = t.value; renderApp(); return; }
    if (t.getAttribute('data-filter') === 'contact-degree') { state.contactDegreeFilter = t.value; renderApp(); return; }
    if (t.getAttribute('data-filter') === 'portal-contact') { state.portalContactId = t.value; renderApp(); return; }

    // Pricing Calculator reactive inputs
    if (['calc-contact','calc-service','calc-qty','calc-complexity','calc-urgency','calc-academic','calc-discount','calc-currency'].includes(t.id)) {
      if (t.id === 'calc-contact') state.calcContactId = t.value;
      if (t.id === 'calc-service') state.calcServiceId = t.value;
      if (t.id === 'calc-qty') state.calcQty = Number(t.value) || 1;
      if (t.id === 'calc-complexity') state.calcComplexity = t.value;
      if (t.id === 'calc-urgency') state.calcUrgency = t.value;
      if (t.id === 'calc-academic') state.calcAcademic = t.value;
      if (t.id === 'calc-discount') state.calcDiscountPct = Number(t.value) || 0;
      if (t.id === 'calc-currency') state.calcCurrency = t.value;
      renderApp();
    }
  });

  document.addEventListener('input', function(e) {
    const t = e.target;
    if (t.id === 'global-search-input') {
      state.searchQuery = t.value;
      const pos = t.selectionStart;
      renderApp();
      const nextInput = document.getElementById('global-search-input');
      if (nextInput) {
        nextInput.focus();
        try { nextInput.setSelectionRange(pos, pos); } catch (_) {}
      }
    }
  });

  // Connect Electron IPC Bridge if running inside Desktop Shell
  if (window.uesDesktopBridge) {
    window.uesDesktopBridge.onNavigate(pg => { const nav=NAV_ITEMS.find(n=>n.id===pg); if(state.authenticated && nav && hasAccess(nav.perm)){ state.page=pg;renderApp();} });
    window.uesDesktopBridge.onRunJourney(() => { if(state.authenticated && state.currentRole==='super_admin') executeCompleteUserJourney(); });
    window.uesDesktopBridge.onToggleTheme(() => { state.darkMode = !state.darkMode; renderApp(); });
    window.uesDesktopBridge.onToggleLang(() => { state.lang = state.lang === 'ar' ? 'en' : 'ar'; renderApp(); });
  }

  // CENTRAL synchronization: only row-level changed records reach the server.
  // Every operation carries a base hash to prevent silently overwriting coworkers' changes.
  let desktopPersistenceReady = false;
  let desktopSaveTimer = null;
  let desktopSaving = false;
  let desktopLastSaved = '';
  let lastServerRevision = 0;
  let baselineDatabase = {};
  let baselineHashes = {};
  let centralSyncConflict = false;
  const localApp = (location.protocol === 'https:' || location.protocol === 'http:');
  const CENTRAL_EXCLUDED = new Set(['users','profiles','roles','permissions','memberships','invitations',
      'activity_logs','payments','integration_connections','webhook_events','channels']);

  function centralChanges() {
    const changes = [];
    for (const [table, rows] of Object.entries(db)) {
      if (CENTRAL_EXCLUDED.has(table) || !Array.isArray(rows)) continue;
      const original = Array.isArray(baselineDatabase[table]) ? baselineDatabase[table] : [];
      const before = new Map(original.filter(r => r && r.id).map(r => [r.id, r]));
      const after = new Map(rows.filter(r => r && r.id).map(r => [r.id, r]));
      for (const [id, record] of after) {
        const previous = before.get(id);
        if (!previous) changes.push({table, op:'insert', id, row:record});
        else if (JSON.stringify(previous)!==JSON.stringify(record))
          changes.push({table, op:'update', id, base_hash:baselineHashes[table]?.[id], row:record});
      }
      for (const [id] of before) if (!after.has(id))
        changes.push({table, op:'delete', id, base_hash:baselineHashes[table]?.[id]});
    }
    return changes;
  }

  async function refreshCentralState(quiet=false) {
    if (!localApp || !state.authenticated || desktopSaving || centralChanges().length) return;
    try {
      const resp=await fetch('/api/state',{cache:'no-store',credentials:'same-origin'});
      if(resp.status===401) { state.authenticated=false;desktopPersistenceReady=false;renderApp();return; }
      if(!resp.ok) throw new Error('HTTP '+resp.status);
      const data=await resp.json();
      if(data.ok && data.database) {
        db=data.database;
        baselineHashes=data.hashes||{};
        lastServerRevision=data.revision||0;
        desktopLastSaved=JSON.stringify(db);
        state.currentProfile=db.profiles.find(p=>p.user_id===state.currentUser?.id)||state.currentProfile;
        state.aiApiKeyConnected=false;
        if(db.agents?.[0]) db.agents[0].connection_mode='غير متصل — محاكاة فقط';
        baselineDatabase=JSON.parse(JSON.stringify(db));
        desktopPersistenceReady=true;centralSyncConflict=false;
        renderApp();
      }
    } catch(e) {
      console.error('Central refresh failed',e);
      if(!quiet) showToast('تعذر الاتصال بسيرفر المتحدة', 'error');
    }
  }

  function scheduleDesktopSave() {
    if (!localApp || !state.authenticated || !desktopPersistenceReady || centralSyncConflict) return;
    const changes=centralChanges();
    if(!changes.length) return;
    clearTimeout(desktopSaveTimer);
    desktopSaveTimer=setTimeout(async ()=>{
      if(desktopSaving) {scheduleDesktopSave();return;}
      const sending=centralChanges();
      if(!sending.length) return;
      desktopSaving=true;
      try {
        const response=await fetch('/api/changes',{
          method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',
          body:JSON.stringify({changes:sending})
        });
        const result=await response.json().catch(()=>({error:'تعذر قراءة رد الخادم'}));
        if(!response.ok) {
          if(response.status===409) centralSyncConflict=true;
          throw new Error(result.error||'فشل الحفظ على الخادم');
        }
        // After successful commit, reload authoritative rows/hashes. Do not pretend an
        // unacknowledged local change was saved; on simultaneous edits, show conflict.
        for(const c of sending) {
          const entries=baselineDatabase[c.table]||[];
          const pos=entries.findIndex(x=>x.id===c.id);
          if(c.op==='delete') {if(pos>=0) entries.splice(pos,1);}
          else if(pos>=0) entries[pos]=JSON.parse(JSON.stringify(c.row));
          else entries.push(JSON.parse(JSON.stringify(c.row)));
        }
        lastServerRevision=result.revision||lastServerRevision;
      } catch(err) {
        console.error('UES server refused changes',err);
        showToast('لم تُحفظ التغييرات: '+err.message+(centralSyncConflict?' — حدّث الصفحة بعد نسخ التعديلات المهمة':''),'error');
      } finally {
        desktopSaving=false;
        if(!centralChanges().length && !centralSyncConflict) await refreshCentralState(true);
      }
    },500);
  }

  async function initializeDesktopState() {
    if(!state.authenticated) {desktopPersistenceReady=false;renderApp();return;}
    // The existing login action gets identity from server, not role selectors.
    await refreshCentralState(false);
  }

  // WebSocket is a fast signal; regular revision polling is a fallback during reconnects.
  function startCentralRealtime() {
    setInterval(async ()=>{
      if(!state.authenticated||!desktopPersistenceReady||desktopSaving||centralChanges().length) return;
      try {
        const response=await fetch('/api/revision',{cache:'no-store'});
        if(response.status===401){state.authenticated=false;desktopPersistenceReady=false;renderApp();return;}
        const data=await response.json();
        if(data.revision>lastServerRevision) await refreshCentralState(true);
      } catch(e) { /* polling retry */ }
    },7000);
    let ws;
    function connect(){
      try {
        ws=new WebSocket((location.protocol==='https:'?'wss://':'ws://')+location.host+'/api/ws');
        ws.onmessage=async evt=>{
          let x;try{x=JSON.parse(evt.data)}catch(_){return}
          if(x.revision>lastServerRevision && !desktopSaving && !centralChanges().length)
            await refreshCentralState(true);
        };
        ws.onclose=()=>setTimeout(connect,5000);
      } catch(e){setTimeout(connect,7000)}
    }
    connect();
  }
  if(localApp) startCentralRealtime();

  renderApp();
  // Private records load only after successful server-authenticated login.

})();
