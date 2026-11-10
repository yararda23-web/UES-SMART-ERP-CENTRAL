#!/usr/bin/env python3
"""Explicit, non-destructive UES SQLite -> central relational DB migration.

DRY RUN is the default and needs no DB connection. For applying, the PostgreSQL
DB must be empty of business rows; users are disabled except owner and all old
password hashes are reset, preventing compromised/demo passwords in production.
"""
import argparse, json, os, sqlite3, sys, secrets
from pathlib import Path
from collections import Counter
from sqlalchemy import MetaData, create_engine, inspect, select, insert, update
from sqlalchemy.orm import Session

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from backend.cloud.app import init_database, engine, RELTABLES, pw_hash, stamp
from backend.cloud.permissions import ALLOWED_TABLES


def load_rows(path, include_ui):
    conn=sqlite3.connect(str(path));conn.row_factory=sqlite3.Row
    names={r['name'] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    tables={t:[dict(x) for x in conn.execute('SELECT * FROM "'+t+'"')] for t in ALLOWED_TABLES if t in names}
    report={'sqlite_tables':len(tables),'row_counts':{t:len(v) for t,v in sorted(tables.items())},'snapshot':{}}
    if include_ui and 'desktop_ui_state' in names:
        one=conn.execute('SELECT snapshot_json FROM desktop_ui_state WHERE id=1').fetchone()
        if one:
            snapshot=json.loads(one['snapshot_json'])
            # Never trust frontend snapshot for identity or payment state.
            blocked={'users','roles','permissions','profiles','memberships','invitations','payments','invoices','activity_logs','webhook_events','integration_connections'}
            for table,items in snapshot.items():
                if table not in tables or table in blocked or not isinstance(items,list):continue
                index={r['id']:r for r in tables[table] if 'id' in r}
                changes=0
                for record in items:
                    if not isinstance(record,dict) or not record.get('id'):continue
                    rid=record['id']
                    if index.get(rid)!=record:changes+=1
                    index[rid]=record
                tables[table]=list(index.values())
                if changes:report['snapshot'][table]={'updated_or_added':changes}
    report['final_counts']={t:len(v) for t,v in sorted(tables.items())}
    return tables,report


def apply(target_data, owner_username, pw_file):
    if engine.dialect.name != 'postgresql':
        raise RuntimeError('APPLY only runs against PostgreSQL. Set DATABASE_URL to the central PostgreSQL service.')
    if not pw_file or not pw_file.is_file():
        raise RuntimeError('Owner password file is required; its content must be at least 14 chars.')
    new_pw=pw_file.read_text('utf8').strip()
    if len(new_pw)<14:raise RuntimeError('Owner password must have >=14 characters')
    init_database()
    with Session(engine) as con:
        count=con.execute(select(RELTABLES['organizations'])).first()
        if count:raise RuntimeError('Central database already contains business data. Refusing to merge or overwrite.')
        # Follow database foreign keys to insert referenced tables before children.
        tables=MetaData();tables.reflect(bind=engine,only=list(RELTABLES))
        for table in tables.sorted_tables:
            name=table.name
            if name not in target_data:continue
            allowed={c.name for c in table.columns}
            for row in target_data[name]:
                clean={k:v for k,v in row.items() if k in allowed}
                if 'organization_id' in allowed and not clean.get('organization_id'):
                    raise RuntimeError(f'{name}: missing organization_id')
                if name=='users':
                    # Stop reuse of any bundled demo credentials; manual activation by Owner.
                    clean['password_hash']=pw_hash(secrets.token_urlsafe(35))
                    clean['is_active']=0
                    clean['failed_attempts']=0
                    clean['locked_until']=None
                    if clean.get('username')==owner_username and clean.get('is_owner'):
                        clean['password_hash']=pw_hash(new_pw)
                        clean['is_active']=1
                con.execute(insert(table).values(**clean))
        owner=con.execute(select(RELTABLES['users']).where(RELTABLES['users'].c.username==owner_username)).mappings().first()
        if not owner or not owner['is_owner'] or owner['role_code']!='super_admin':
            raise RuntimeError('Owner username not found or not owner; all inserts rolled back.')
        con.commit()
        return {'owner':owner_username,'imported_rows':{t:len(v) for t,v in target_data.items()},'disabled_nonowner_accounts':True}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sqlite',required=True,type=Path,help='Path to actual SQLite user data backup (.db)')
    p.add_argument('--include-ui-snapshot',action='store_true',help='Merge desktop_ui_state UI records, except financial and identity records')
    p.add_argument('--apply',action='store_true',help='Actually migrate into an EMPTY central PostgreSQL database')
    p.add_argument('--owner-username',default='Ahmed_99')
    p.add_argument('--owner-password-file',type=Path)
    p.add_argument('--report',type=Path,default=Path('migration_report.json'))
    args=p.parse_args()
    if not args.sqlite.is_file():p.error('SQLite source file not found')
    tables,report=load_rows(args.sqlite,args.include_ui_snapshot)
    report['mode']='apply' if args.apply else 'dry-run'
    report['source_path']=str(args.sqlite)
    if args.apply:
        report['result']=apply(tables,args.owner_username,args.owner_password_file)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
