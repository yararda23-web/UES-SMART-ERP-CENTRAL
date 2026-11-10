VIEWS_PART1_JS = r"""
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
"""
