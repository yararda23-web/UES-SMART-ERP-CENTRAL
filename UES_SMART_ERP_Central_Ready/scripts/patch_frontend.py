from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'frontend/src/events_part.py'
s=p.read_text('utf8')
start=s.index('  // Desktop local persistence:')
end=s.index('  renderApp();\n  // Private records load only after successful server-authenticated login.',start)
replacement=r'''  // CENTRAL synchronization: only row-level changed records reach the server.
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
        baselineDatabase=JSON.parse(JSON.stringify(db));
        baselineHashes=data.hashes||{};
        lastServerRevision=data.revision||0;
        desktopLastSaved=JSON.stringify(db);
        state.currentProfile=db.profiles.find(p=>p.user_id===state.currentUser?.id)||state.currentProfile;
        state.aiApiKeyConnected=false;
        if(db.agents?.[0]) db.agents[0].connection_mode='غير متصل — محاكاة فقط';
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

'''
s=s[:start]+replacement+s[end:]
# Replace local-only payment handler with authorized server-side transactional confirmation.
start=s.index("      } else if (subType === 'save-payment') {")
end=s.index("      } else if (subType === 'save-expense') {",start)
replacement2=r'''      } else if (subType === 'save-payment') {
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
'''
s=s[:start]+replacement2+s[end:]
p.write_text(s,'utf8')

p=root/'frontend/src/core_js_part.py';s=p.read_text('utf8')
s=s.replace("    if (!db.roles.some(r => r.code === state.currentRole)) return false;\n", "    // Do not require full roles listing; only owner may download it.\n")
p.write_text(s,'utf8')
