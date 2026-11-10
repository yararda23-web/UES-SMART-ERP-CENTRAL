CORE_JS = r"""
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
"""
