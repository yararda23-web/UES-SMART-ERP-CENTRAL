HANDLERS_JS = r"""
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
"""
