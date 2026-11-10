"""UES Smart ERP Central API — PostgreSQL production target, SQLite test adapter.

One authority for identities, customer data and financial actions. Client-side snapshots
are never accepted as full-table replacements. Changes are per-row, conflict checked.
Not a certified accounting system or external-message integration.
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import (Table, Column, Integer, Text, DateTime, MetaData,
                        create_engine, inspect, select, update, insert, delete, text)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .permissions import (ALLOWED_TABLES, IDENTITY_TABLES, PUBLIC_NAMES,
                          ROLE_READ, ROLE_WRITE, PROTECTED_WRITE)

APP_ROOT = Path(__file__).resolve().parents[2]
FRONTEND = Path(os.getenv('UES_FRONTEND_PATH', str(APP_ROOT / 'frontend' / 'dist')))
SCHEMA_FILE = APP_ROOT / 'database' / 'schema.sql'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///'+str(APP_ROOT/'database'/'test_central_dev.sqlite'))
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL='postgresql+psycopg://'+DATABASE_URL[len('postgres://'):]
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL='postgresql+psycopg://'+DATABASE_URL[len('postgresql://'):]
PUBLIC_URL = os.getenv('UES_PUBLIC_URL', 'http://127.0.0.1:8000').rstrip('/')
SESSION_TTL = 8*60*60
COOKIE_NAME = 'UES_SESSION'
PROTECTED_SECRETS = ('secret', 'token', 'api_key', 'password', 'credential', 'config_json', 'auth_code')

def utcnow():
    return datetime.now(timezone.utc)

def stamp():
    return utcnow().strftime('%Y-%m-%d %H:%M:%S')

def digest(value: str) -> str:
    return hashlib.sha256(value.encode('utf8')).hexdigest()

def row_digest(value: dict[str, Any]) -> str:
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':'), default=str))

def pw_hash(password: str) -> str:
    salt = secrets.token_bytes(16); iters=600_000
    dk = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,iters)
    return f'pbkdf2_sha256${iters}${salt.hex()}${dk.hex()}'

def pw_verify(password: str, stored: str) -> bool:
    if not stored or not stored.startswith('pbkdf2_sha256$'): return False
    try:
        _, rounds, salt, raw = stored.split('$')
        return hmac.compare_digest(hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),int(rounds)),bytes.fromhex(raw))
    except (ValueError,TypeError): return False

kwargs = {'pool_pre_ping':True}
if DATABASE_URL.startswith('sqlite:'):
    kwargs['connect_args']={'check_same_thread':False}
engine = create_engine(DATABASE_URL, **kwargs)
meta = MetaData()
sessions = Table('ues_sessions', meta,
    Column('token_hash',Text,primary_key=True), Column('user_id',Text,nullable=False),
    Column('org_id',Text,nullable=False), Column('expires_at',DateTime(timezone=True),nullable=False))
events = Table('ues_events',meta,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('org_id',Text,nullable=False,index=True), Column('actor_id',Text,nullable=False),
    Column('event_type',Text,nullable=False), Column('created_at',DateTime(timezone=True),nullable=False))
RELTABLES={}
TABLE_ORDER=[]


def init_database():
    """Idempotent schema creation; NEVER seeds demo data or overwrites a database."""
    from sqlalchemy import event as saevent
    if engine.dialect.name=='sqlite':
        @saevent.listens_for(engine,'connect')
        def _sqlite_pragma(dbapi_con, _): dbapi_con.execute('PRAGMA foreign_keys=ON')
    existing=set(inspect(engine).get_table_names())
    if 'organizations' not in existing:
        ddl=SCHEMA_FILE.read_text('utf8').replace('PRAGMA foreign_keys = ON;', '')
        with engine.begin() as con:
            # No executable triggers in this schema: CREATE TABLE / CREATE INDEX only.
            for stmt in ddl.split(';'):
                if stmt.strip() and re.search(r'\bCREATE\s+(?:TABLE|INDEX)\b',stmt,re.I):
                    # leading SQL comments are fine for PostgreSQL and SQLite
                    con.exec_driver_sql(stmt.strip())
    meta.create_all(engine, checkfirst=True)
    meta.reflect(bind=engine, only=[t for t in ALLOWED_TABLES if inspect(engine).has_table(t)])
    RELTABLES.update({k:meta.tables[k] for k in ALLOWED_TABLES if k in meta.tables})
    # Dependency-safe parent-first order for batched relational changes.
    global TABLE_ORDER
    TABLE_ORDER=[t.name for t in meta.sorted_tables if t.name in RELTABLES]


@asynccontextmanager
async def lifespan(app:FastAPI):
    if os.getenv('UES_REQUIRE_POSTGRES','false').lower()=='true' and engine.dialect.name!='postgresql':
        raise RuntimeError('Production requires DATABASE_URL configured for PostgreSQL')
    init_database()
    yield

app=FastAPI(title='UES Smart ERP Central API', version='3.0.0', lifespan=lifespan, docs_url=None, redoc_url=None)
allowed_hosts=[h.strip() for h in os.getenv('UES_ALLOWED_HOSTS','localhost,127.0.0.1').split(',') if h.strip()]
app.add_middleware(TrustedHostMiddleware,allowed_hosts=allowed_hosts)


def error(status:int, msg:str):
    raise HTTPException(status_code=status,detail=msg)

@app.exception_handler(HTTPException)
async def http_error(request:Request,ex:HTTPException):
    return JSONResponse({'ok':False,'error':str(ex.detail)},status_code=ex.status_code,headers={'Cache-Control':'no-store'})


def verify_origin(req:Request):
    origin=req.headers.get('origin')
    # Local tests may omit Origin; browsers send it on cross-origin POSTs.
    if origin and origin != str(req.base_url).rstrip('/') and origin != PUBLIC_URL:
        error(403,'Cross-origin requests blocked')
    sec_site=req.headers.get('sec-fetch-site','')
    if sec_site not in ('','same-origin','none'):
        error(403,'Cross-site requests blocked')
    if req.headers.get('content-type','').split(';')[0] != 'application/json':
        error(415,'JSON required')


def current_user(req:Request, con:Session) -> dict:
    token=req.cookies.get(COOKIE_NAME,'')
    if not token: error(401,'سجل الدخول أولاً')
    s=con.execute(select(sessions).where(sessions.c.token_hash==digest(token))).mappings().first()
    if not s: error(401,'جلسة غير صالحة')
    expiry=s['expires_at']
    if expiry.tzinfo is None: expiry=expiry.replace(tzinfo=timezone.utc)
    if expiry<=utcnow(): error(401,'انتهت صلاحية الجلسة')
    u=con.execute(select(RELTABLES['users']).where(RELTABLES['users'].c.id==s['user_id'])).mappings().first()
    if not u or not u['is_active'] or u['organization_id']!=s['org_id']: error(401,'المستخدم غير نشط')
    return dict(u)


def owner_only(u):
    if u['role_code']!='super_admin' or not u['is_owner']: error(403,'المالك فقط')


def safe_user(u):
    return {k:u[k] for k in PUBLIC_NAMES if k in u}


def conn_rows(con:Session,table:str,org:str)->list[dict]:
    t=RELTABLES[table]
    stmt=select(t)
    if 'organization_id' in t.c: stmt=stmt.where(t.c.organization_id==org)
    return [dict(x) for x in con.execute(stmt).mappings().all()]


def scoped(table, rows, user, all_rows):
    role=user['role_code']; uid=user['id']
    if role=='academic_specialist':
        proj={x.get('project_id') for x in all_rows.get('project_members',[]) if x.get('user_id')==uid}
        proj.update(x.get('project_id') for x in all_rows.get('tasks',[]) if x.get('assigned_to')==uid)
        if table=='tasks': return [r for r in rows if r.get('assigned_to')==uid]
        if table=='projects': return [r for r in rows if r.get('id') in proj]
        if table=='project_members': return [r for r in rows if r.get('project_id') in proj]
        if table=='files': return [r for r in rows if r.get('project_id') in proj and r.get('access_level')!='داخلي سري']
        if table=='contacts':
            contact_ids={r.get('contact_id') for r in all_rows.get('projects',[]) if r.get('id') in proj}
            return [r for r in rows if r.get('id') in contact_ids]
    if role=='client':
        permitted={r.get('contact_id') for r in all_rows.get('client_portal_access',[]) if r.get('user_id')==uid}
        projs={r.get('id') for r in all_rows.get('projects',[]) if r.get('contact_id') in permitted}
        contracts={r.get('id') for r in all_rows.get('contracts',[]) if r.get('contact_id') in permitted}
        invoice_ids={r.get('id') for r in all_rows.get('invoices',[]) if r.get('contract_id') in contracts}
        scope_map={
            'client_portal_access':lambda r:r.get('user_id')==uid,
            'contacts':lambda r:r.get('id') in permitted,
            'projects':lambda r:r.get('id') in projs,
            'contracts':lambda r:r.get('id') in contracts,
            'contract_milestones':lambda r:r.get('contract_id') in contracts,
            'tasks':lambda r:r.get('project_id') in projs,
            'invoices':lambda r:r.get('id') in invoice_ids,
            'payments':lambda r:r.get('invoice_id') in invoice_ids,
            'files':lambda r:r.get('project_id') in projs and r.get('access_level')!='داخلي سري'
        }
        return list(filter(scope_map.get(table,lambda _:False),rows))
    return rows


def visible_state(con,u):
    role=u['role_code']; visible=set(ALLOWED_TABLES) if role=='super_admin' else ROLE_READ.get(role,set())
    # Specialist scoping needs membership and project refs even if not visible.
    required=visible|{'projects','project_members','tasks','client_portal_access','invoices','contracts'}
    data={t:conn_rows(con,t,u['organization_id']) for t in required if t in RELTABLES}
    output={}
    for t in ALLOWED_TABLES:
        rows=scoped(t,data.get(t,[]),u,data) if t in visible else []
        if t=='users': rows=[safe_user(row) for row in rows]
        if t=='profiles' and role!='super_admin': rows=[r for r in rows if r.get('user_id')==u['id']]
        if t in {'channels','integration_connections'}:
            rows=[{k:v for k,v in r.items() if not any(s in k.lower() for s in PROTECTED_SECRETS)} for r in rows]
        output[t]=rows
    if role!='super_admin':
        output['users']=[safe_user(u)]
        output['roles']=[];output['permissions']=[];output['memberships']=[]
        output['profiles']=[r for r in data.get('profiles',[]) if r.get('user_id')==u['id']]
    return output


def audit(con,u,action,entity_type='',entity_id=''):
    t=RELTABLES['activity_logs']
    con.execute(insert(t).values(id='LOG-C-'+secrets.token_hex(9),organization_id=u['organization_id'],
      actor_name=u['username'],actor_role=u['role_code'],category='سجل المزامنة',
      action_summary=action[:450],entity_type=entity_type,entity_id=entity_id,created_at=stamp()))


def new_event(con,u,kind):
    con.execute(insert(events).values(org_id=u['organization_id'],actor_id=u['id'],event_type=kind,created_at=utcnow()))


def event_revision(con,org):
    return con.execute(text('SELECT COALESCE(MAX(id),0) FROM ues_events WHERE org_id=:org'),{'org':org}).scalar_one()


@app.get('/api/health')
def health():
    try:
        with Session(engine) as con: con.execute(text('SELECT 1')).scalar_one()
    except SQLAlchemyError: error(503,'Database unavailable')
    return {'ok':True,'service':'UES-SMART-ERP-CENTRAL','database':engine.dialect.name,'version':'3.0.0'}

@app.get('/')
def root():
    f=FRONTEND/'UES_SMART_ERP.html'
    if not f.is_file(): error(500,'Build frontend first: npm run build:web')
    return FileResponse(f,media_type='text/html',headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'})

@app.get('/assets/ues-app.js')
def frontend_script():
    f=FRONTEND/'assets'/'ues-app.js'
    if not f.is_file(): error(500,'JavaScript build missing')
    return FileResponse(f,media_type='application/javascript',headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'})

@app.get('/assets/ues.css')
def css():
    f=FRONTEND/'assets'/'ues.css'
    if not f.is_file(): error(500,'CSS missing')
    return FileResponse(f,media_type='text/css')

class Login(BaseModel):
    username:str=Field(min_length=1,max_length=150)
    password:str=Field(min_length=1,max_length=300)

@app.post('/api/auth/login')
def login(body:Login,req:Request,response:Response):
    verify_origin(req)
    t=RELTABLES['users']
    with Session(engine) as con:
        # Choose user solely by login, never by the client-selected portal/role.
        u=con.execute(select(t).where((t.c.username==body.username)|(t.c.email==body.username))).mappings().first()
        if not u: error(401,'اسم المستخدم أو كلمة المرور غير صحيحة')
        if not u['is_active']: error(403,'الحساب موقوف')
        locked=u.get('locked_until')
        if locked and str(locked)>stamp(): error(429,'الحساب مقفل مؤقتًا')
        good=pw_verify(body.password,u['password_hash'])
        if not good:
            failures=int(u.get('failed_attempts') or 0)+1
            values={'failed_attempts':failures}
            if failures>=5: values['locked_until']=(utcnow()+timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            con.execute(update(t).where(t.c.id==u['id']).values(**values));con.commit()
            error(401,'اسم المستخدم أو كلمة المرور غير صحيحة')
        con.execute(update(t).where(t.c.id==u['id']).values(failed_attempts=0,locked_until=None,last_login_at=stamp()))
        token=secrets.token_urlsafe(48)
        con.execute(insert(sessions).values(token_hash=digest(token),user_id=u['id'],org_id=u['organization_id'],expires_at=utcnow()+timedelta(seconds=SESSION_TTL)))
        con.commit()
        response.set_cookie(COOKIE_NAME,token,max_age=SESSION_TTL,httponly=True,secure=PUBLIC_URL.startswith('https://'),samesite='strict',path='/')
        return {'ok':True,'user':safe_user(u)}

@app.get('/api/auth/session')
def get_session(req:Request):
    with Session(engine) as con: return {'ok':True,'user':safe_user(current_user(req,con))}

@app.post('/api/auth/logout')
def logout(req:Request,response:Response):
    verify_origin(req)
    token=req.cookies.get(COOKIE_NAME,'')
    with Session(engine) as con:
        if token: con.execute(delete(sessions).where(sessions.c.token_hash==digest(token)));con.commit()
    response.delete_cookie(COOKIE_NAME,path='/')
    return {'ok':True}

class PasswordChange(BaseModel):
    old_password:str
    new_password:str=Field(min_length=12,max_length=300)

@app.post('/api/auth/change-password')
def change_password(body:PasswordChange,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        u=current_user(req,con)
        if not pw_verify(body.old_password,u['password_hash']): error(403,'كلمة المرور الحالية خاطئة')
        if body.old_password==body.new_password: error(400,'أدخل كلمة مرور مختلفة')
        con.execute(update(RELTABLES['users']).where(RELTABLES['users'].c.id==u['id']).values(password_hash=pw_hash(body.new_password),updated_at=stamp()))
        con.execute(delete(sessions).where(sessions.c.user_id==u['id']).where(sessions.c.token_hash!=digest(req.cookies.get(COOKIE_NAME,''))))
        audit(con,u,'تغيير كلمة المرور','users',u['id']);con.commit()
    return {'ok':True}

@app.get('/api/state')
def get_state(req:Request):
    with Session(engine) as con:
        u=current_user(req,con); data=visible_state(con,u)
        hashes={t:{r['id']:row_digest(r) for r in rows if 'id' in r} for t,rows in data.items()}
        return {'ok':True,'database':data,'hashes':hashes,'revision':event_revision(con,u['organization_id'])}

@app.get('/api/revision')
def get_revision(req:Request):
    with Session(engine) as con:
        u=current_user(req,con)
        return {'ok':True,'revision':event_revision(con,u['organization_id'])}

class Change(BaseModel):
    table:str
    op:str
    id:str
    base_hash:str|None=None
    row:dict[str,Any]|None=None
class Changes(BaseModel):
    changes:list[Change]=Field(max_length=150)

CRITICAL_FIELDS={
  'users':{'role_code','password_hash','is_owner','is_active','failed_attempts'},
  'invoices':{'paid_cents','remaining_cents','status'},
  'quotes':{'status','discount_pct','total_cents','tax_cents','discount_cents'},
  'contracts':{'approval_status','signature_status','contract_value_cents'},
  'projects':set(),
}


def allowed_mutation(u, table, op, old, row, con):
    role=u['role_code']; uid=u['id']; org=u['organization_id']
    writable=(ALLOWED_TABLES-PROTECTED_WRITE) if role=='super_admin' else set(ROLE_WRITE.get(role,set()))
    if table=='approvals' and role in ('sales_rep','customer_support') and op=='insert': writable.add('approvals')
    if table not in writable or table in PROTECTED_WRITE:
        error(403,'تعديل هذا القسم غير مسموح: '+table)
    if table in {'integration_connections','channels','webhook_events'}: error(403,'إعدادات الاتصالات عبر إجراءات إدارية آمنة فقط')
    if table=='automation_rules' and role!='super_admin': error(403,'إعدادات الأتمتة للمالك فقط')
    if table=='organizations' and role!='super_admin': error(403,'بيانات المؤسسة للمالك فقط')
    if table=='invoices' and role not in ('finance_manager','super_admin'): error(403,'الفواتير للمالية فقط')
    if table=='invoices' and op=='insert' and row and (int(row.get('paid_cents') or 0)!=0 or int(row.get('remaining_cents') or 0)!=int(row.get('amount_cents') or 0)):
        error(403,'الفاتورة الجديدة يجب أن تبدأ برصيد غير محصل')
    if table=='quotes':
        if role=='sales_rep' and row and (row.get('status') or 'مسودة') not in ('مسودة','بانتظار الاعتماد'): error(403,'اعتماد العرض يتطلب مدير مبيعات')
        if old and row and old.get('status')!=row.get('status') and role not in ('super_admin','sales_manager','general_manager'):
            error(403,'تغيير حالة العرض يحتاج موافقة مدير')
        if row and float(row.get('discount_pct') or 0)>10 and role not in ('super_admin','sales_manager'):
            error(403,'الخصم غير المصرح يتطلب موافقة')
    if table=='invoices' and old and row and any(old.get(k)!=row.get(k) for k in CRITICAL_FIELDS['invoices']):
        error(403,'لا يجوز تغيير الرصيد أو الدفع من واجهة عامة؛ استخدم عملية المالية')
    if table=='contracts' and old and row and any(old.get(k)!=row.get(k) for k in CRITICAL_FIELDS['contracts']):
        error(403,'اعتماد العقود يتطلب إجراء مفوض')
    if role=='academic_specialist':
        if table!='tasks': error(403,'التعديل مسموح للمهام المسندة فقط')
        if not old or old.get('assigned_to')!=uid: error(403,'المهمة غير مسندة إليك')
        if row and any(old.get(k)!=row.get(k) for k in (set(old)|set(row))-{'status','progress_pct','updated_at'}):
            error(403,'تعديل غير مسموح على المهمة')
    if table=='approvals' and role in ('sales_rep','customer_support'):
        if op!='insert' or not row or row.get('status')!='قيد الانتظار' or row.get('decided_by'):
            error(403,'يمكن للمبيعات طلب الموافقة فقط')
    if table=='payments': error(403,'تأكيد المدفوعات عبر المالية فقط')


def serial_values(tbl, record):
    if not record or not isinstance(record,dict): error(400,'بيانات السجل غير صحيحة')
    names=set(tbl.c.keys())
    if set(record)-names: error(400,'حقول غير معروفة: '+','.join(set(record)-names))
    return {k:v for k,v in record.items() if k in names}

@app.post('/api/changes')
async def save_changes(payload:Changes,req:Request):
    verify_origin(req)
    if not payload.changes: return {'ok':True,'changes':0}
    with Session(engine) as con:
        u=current_user(req,con)
        # Order parents before dependent children for inserts; deletes reversed.
        order=TABLE_ORDER
        changes=sorted(payload.changes,key=lambda c:(c.op=='delete', -order.index(c.table) if c.op=='delete' and c.table in order else order.index(c.table) if c.table in order else 999))
        for change in changes:
            table=change.table
            if table not in RELTABLES or table not in ALLOWED_TABLES or not re.fullmatch(r'[A-Za-z0-9_]{1,60}',table): error(400,'Unknown resource')
            if not change.id or len(change.id)>200: error(400,'Invalid identifier')
            tbl=RELTABLES[table]
            cond=tbl.c.id==change.id
            if 'organization_id' in tbl.c: cond=cond & (tbl.c.organization_id==u['organization_id'])
            existing=con.execute(select(tbl).where(cond)).mappings().first()
            old=dict(existing) if existing else None
            if change.op=='insert':
                if old: error(409,'سجل موجود بالفعل؛ حدث بياناتك')
                row=serial_values(tbl,change.row)
                if row.get('id')!=change.id: error(400,'ID mismatch')
                if 'organization_id' in tbl.c and row.get('organization_id')!=u['organization_id']:
                    error(403,'Organization mismatch')
                allowed_mutation(u,table,'insert',None,row,con)
                con.execute(insert(tbl).values(**row))
            elif change.op in ('update','delete'):
                if not old: error(409,'السجل تغير أو حذف بواسطة مستخدم آخر')
                # base_hash proves the client updated precisely this version.
                if not change.base_hash or row_digest(old)!=change.base_hash: error(409,'تم تعديل البيانات على جهاز آخر؛ حدث الصفحة وحاول مجددًا')
                if change.op=='delete':
                    allowed_mutation(u,table,'delete',old,None,con)
                    con.execute(delete(tbl).where(cond))
                else:
                    row=serial_values(tbl,change.row)
                    if row.get('id')!=change.id or ('organization_id' in tbl.c and row.get('organization_id')!=u['organization_id']): error(403,'Immutable ID/organization')
                    allowed_mutation(u,table,'update',old,row,con)
                    changed={k:v for k,v in row.items() if k not in ('id','organization_id') and old.get(k)!=v}
                    if changed: con.execute(update(tbl).where(cond).values(**changed))
            else: error(400,'Bad operation')
            audit(con,u,f'{change.op} {table} {change.id}',table,change.id)
        new_event(con,u,'records.changed')
        try: con.commit()
        except IntegrityError: error(409,'Database constraint violation; no changes were saved')
        version=event_revision(con,u['organization_id'])
    await hub.broadcast(u['organization_id'],{'type':'changed','revision':version})
    return {'ok':True,'changes':len(changes),'revision':version}

class NewUser(BaseModel):
    username:str=Field(min_length=3,max_length=80)
    email:str=Field(min_length=5,max_length=200)
    password:str=Field(min_length=12,max_length=300)
    role_code:str=Field(min_length=2,max_length=80)
    full_name:str=Field(min_length=2,max_length=120)
    department:str='عام'
    job_title:str='موظف'

@app.post('/api/admin/users/create')
def add_user(body:NewUser,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        u=current_user(req,con);owner_only(u)
        if body.role_code=='super_admin': error(403,'لا يمكن إنشاء مالك آخر من الواجهة')
        t=RELTABLES['users'];r=RELTABLES['roles'];p=RELTABLES['profiles'];m=RELTABLES['memberships']
        role=con.execute(select(r).where(r.c.code==body.role_code).where(r.c.organization_id==u['organization_id'])).mappings().first()
        if not role: error(400,'الدور غير موجود')
        now=stamp(); user_id='U-C-'+secrets.token_hex(8)
        con.execute(insert(t).values(id=user_id,organization_id=u['organization_id'],username=body.username,email=body.email,password_hash=pw_hash(body.password),role_code=body.role_code,is_owner=0,is_active=1,mfa_enabled=0,failed_attempts=0,created_at=now,updated_at=now,created_by=u['id']))
        con.execute(insert(p).values(id='PROF-C-'+secrets.token_hex(8),user_id=user_id,organization_id=u['organization_id'],full_name=body.full_name,department=body.department,job_title=body.job_title,created_at=now,updated_at=now,created_by=u['id']))
        con.execute(insert(m).values(id='MEM-C-'+secrets.token_hex(8),organization_id=u['organization_id'],user_id=user_id,role_id=role['id'],status='active',joined_at=now,created_by=u['id']))
        audit(con,u,'إنشاء حساب '+body.username,'users',user_id)
        new_event(con,u,'users.created')
        try:con.commit()
        except IntegrityError:error(409,'اسم المستخدم أو البريد مستخدم بالفعل')
    return {'ok':True,'username':body.username,'role_code':body.role_code}

class ResetPassword(BaseModel):
    user_id:str
@app.post('/api/admin/users/reset-password')
def reset_pw(body:ResetPassword,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        u=current_user(req,con);owner_only(u)
        t=RELTABLES['users']
        target=con.execute(select(t).where(t.c.id==body.user_id).where(t.c.organization_id==u['organization_id'])).mappings().first()
        if not target: error(404,'المستخدم غير موجود')
        temp_pw=secrets.token_urlsafe(21)
        con.execute(update(t).where(t.c.id==body.user_id).values(password_hash=pw_hash(temp_pw),failed_attempts=0,locked_until=None,updated_at=stamp()))
        con.execute(delete(sessions).where(sessions.c.user_id==body.user_id))
        audit(con,u,'إعادة تعيين كلمة مرور موظف','users',body.user_id)
        con.commit()
    return {'ok':True,'temporary_password':temp_pw}

class DeleteRole(BaseModel):
    role_code:str
    replacement_role:str=''
class StaffRoleChange(BaseModel):
    user_id:str
    role_code:str
@app.post('/api/admin/users/set-role')
def staff_role_change(body:StaffRoleChange,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        owner=current_user(req,con);owner_only(owner)
        users=RELTABLES['users'];roles=RELTABLES['roles'];members=RELTABLES['memberships']
        target=con.execute(select(users).where(users.c.id==body.user_id).where(users.c.organization_id==owner['organization_id'])).mappings().first()
        if not target or target['is_owner'] or target['id']==owner['id']: error(403,'لا يمكن تعديل صلاحيات المالك')
        if body.role_code=='super_admin':error(403,'لا يمكن إنشاء سوبر أدمن آخر')
        role=con.execute(select(roles).where(roles.c.code==body.role_code).where(roles.c.organization_id==owner['organization_id'])).mappings().first()
        if not role:error(400,'الدور المطلوب غير موجود')
        con.execute(update(users).where(users.c.id==body.user_id).values(role_code=body.role_code,updated_at=stamp()))
        con.execute(update(members).where(members.c.user_id==body.user_id).values(role_id=role['id']))
        con.execute(delete(sessions).where(sessions.c.user_id==body.user_id))
        audit(con,owner,'تغيير دور موظف إلى '+body.role_code,'users',body.user_id)
        new_event(con,owner,'users.role_changed');con.commit()
    return {'ok':True,'role_code':body.role_code}

class EnableUser(BaseModel):
    user_id:str
@app.post('/api/admin/users/activate')
def activate_user(body:EnableUser,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        owner=current_user(req,con);owner_only(owner)
        users=RELTABLES['users']
        target=con.execute(select(users).where(users.c.id==body.user_id).where(users.c.organization_id==owner['organization_id'])).mappings().first()
        if not target or target['is_owner']:error(403,'الحساب غير صالح للتفعيل')
        temp=secrets.token_urlsafe(22)
        con.execute(update(users).where(users.c.id==body.user_id).values(is_active=1,password_hash=pw_hash(temp),failed_attempts=0,locked_until=None,updated_at=stamp()))
        con.execute(delete(sessions).where(sessions.c.user_id==body.user_id))
        audit(con,owner,'تفعيل حساب موظف بكلمة مؤقتة','users',body.user_id)
        new_event(con,owner,'users.activated');con.commit()
    return {'ok':True,'temporary_password':temp}

@app.post('/api/admin/roles/delete')
def role_delete(body:DeleteRole,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        u=current_user(req,con);owner_only(u)
        if body.role_code=='super_admin': error(400,'دور المالك محمي')
        rt=RELTABLES['roles'];ut=RELTABLES['users'];mt=RELTABLES['memberships'];pt=RELTABLES['permissions'];it=RELTABLES['invitations']
        old=con.execute(select(rt).where(rt.c.code==body.role_code).where(rt.c.organization_id==u['organization_id'])).mappings().first()
        if not old:error(404,'الدور غير موجود')
        users=con.execute(select(ut).where(ut.c.role_code==body.role_code).where(ut.c.organization_id==u['organization_id'])).mappings().all()
        if users:
            new=con.execute(select(rt).where(rt.c.code==body.replacement_role).where(rt.c.organization_id==u['organization_id'])).mappings().first()
            if not new or body.replacement_role in ('super_admin',body.role_code):error(400,'حدد دورًا بديلًا صحيحًا')
            con.execute(update(ut).where(ut.c.role_code==body.role_code).where(ut.c.organization_id==u['organization_id']).values(role_code=body.replacement_role,updated_at=stamp()))
            con.execute(update(mt).where(mt.c.role_id==old['id']).values(role_id=new['id']))
            con.execute(update(it).where(it.c.role_code==body.role_code).where(it.c.organization_id==u['organization_id']).values(role_code=body.replacement_role))
        con.execute(delete(pt).where(pt.c.role_id==old['id']))
        con.execute(delete(rt).where(rt.c.id==old['id']))
        audit(con,u,'حذف دور '+body.role_code,'roles',old['id'])
        new_event(con,u,'roles.deleted');con.commit()
    return {'ok':True,'deleted_role':body.role_code,'reassigned_users':len(users)}

class ConfirmPayment(BaseModel):
    invoice_id:str
    amount_cents:int=Field(gt=0)
    payment_method:str=Field(min_length=2,max_length=100)
    reference_number:str=Field(min_length=3,max_length=150)
    proof_document:str|None=None

@app.post('/api/finance/payments/confirm')
async def confirm_payment(body:ConfirmPayment,req:Request):
    verify_origin(req)
    with Session(engine) as con:
        u=current_user(req,con)
        if u['role_code'] not in ('finance_manager','super_admin'):error(403,'المالية فقط')
        it=RELTABLES['invoices'];pt=RELTABLES['payments']
        invoice=con.execute(select(it).where(it.c.id==body.invoice_id).where(it.c.organization_id==u['organization_id']).with_for_update()).mappings().first()
        if not invoice:error(404,'الفاتورة غير موجودة')
        existing=con.execute(select(pt).where(pt.c.reference_number==body.reference_number)).mappings().first()
        if existing:error(409,'رقم العملية مسجل بالفعل')
        if invoice['remaining_cents']<body.amount_cents:error(400,'قيمة الدفعة أكبر من المتبقي')
        now=stamp(); pid='PAY-C-'+secrets.token_hex(8)
        con.execute(insert(pt).values(id=pid,organization_id=u['organization_id'],payment_number=pid,invoice_id=invoice['id'],contact_id=invoice['contact_id'],amount_cents=body.amount_cents,currency=invoice['currency'],payment_method=body.payment_method,reference_number=body.reference_number,proof_document=body.proof_document,verification_source='finance_officer',verified_by=u['id'],paid_at=now,created_at=now,created_by=u['id']))
        remain=invoice['remaining_cents']-body.amount_cents
        con.execute(update(it).where(it.c.id==invoice['id']).values(remaining_cents=remain,paid_cents=invoice['paid_cents']+body.amount_cents,status='مدفوعة' if remain==0 else 'مدفوعة جزئياً',updated_at=now))
        audit(con,u,'تأكيد دفعة '+pid,'payments',pid);new_event(con,u,'payments.confirmed');con.commit()
        ver=event_revision(con,u['organization_id'])
    await hub.broadcast(u['organization_id'],{'type':'changed','revision':ver})
    return {'ok':True,'payment_id':pid,'revision':ver}

class Hub:
    def __init__(self): self.clients=defaultdict(set)
    async def broadcast(self,org,payload):
        for ws in list(self.clients[org]):
            try:await ws.send_json(payload)
            except Exception:self.clients[org].discard(ws)
hub=Hub()

@app.websocket('/api/ws')
async def ws_endpoint(ws:WebSocket):
    if ws.headers.get('origin') not in (None,'',PUBLIC_URL):
        await ws.close(code=1008);return
    # Validate HTTP-only session cookie, not a user-controlled role parameter.
    fake_req=type('Req',(),{'cookies':ws.cookies})()
    try:
        with Session(engine) as con: u=current_user(fake_req,con)
    except HTTPException:
        await ws.close(code=1008);return
    await ws.accept(); org=u['organization_id'];hub.clients[org].add(ws)
    try:
        while True:
            await asyncio.wait_for(ws.receive_text(),timeout=60)
    except (WebSocketDisconnect,asyncio.TimeoutError):pass
    finally:hub.clients[org].discard(ws)
