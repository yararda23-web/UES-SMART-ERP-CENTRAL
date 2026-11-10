VIEWS_PART2_JS = r"""
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
"""
