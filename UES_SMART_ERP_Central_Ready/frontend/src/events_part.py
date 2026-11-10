EVENTS_JS = r"""
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
"""
