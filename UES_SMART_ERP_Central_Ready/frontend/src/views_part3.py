VIEWS_PART3_JS = r"""
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

"""
