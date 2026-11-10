"""Isolated tests: never connect to or alter the production database."""
import importlib, os, shutil, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class CentralAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        db=Path(cls.tmp.name)/'test.db'
        shutil.copy2(ROOT/'database'/'ues_smart_erp.db',db)
        os.environ['DATABASE_URL']='sqlite:///'+str(db)
        os.environ['UES_PUBLIC_URL']='http://testserver'
        os.environ['UES_ALLOWED_HOSTS']='testserver,localhost'
        sys.path.insert(0,str(ROOT))
        from backend.cloud.app import init_database, engine, RELTABLES, pw_hash
        from sqlalchemy import update
        from sqlalchemy.orm import Session
        init_database()
        cls.engine=engine;cls.tables=RELTABLES
        with Session(engine) as con:
            users=RELTABLES['users']
            for name in ('Ahmed_99','sales_karim','finance_nada'):
                row=con.execute(users.select().where(users.c.username==name)).mappings().first()
                if row:
                    con.execute(update(users).where(users.c.id==row['id']).values(is_active=1,password_hash=pw_hash('StrongTestPass123!')))
            con.commit()
        from fastapi.testclient import TestClient
        from backend.cloud.app import app
        cls.client=TestClient(app)
        cls.client.__enter__()
    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None,None,None);cls.engine.dispose();cls.tmp.cleanup()

    def setUp(self):
        self.client.cookies.clear()
    def login(self,user='Ahmed_99'):
        r=self.client.post('/api/auth/login',json={'username':user,'password':'StrongTestPass123!'})
        self.assertEqual(r.status_code,200,r.text)
        return r.json()

    def test_01_auth_and_permissions(self):
        self.login('sales_karim')
        state=self.client.get('/api/state').json()['database']
        self.assertNotIn('password_hash',str(state.get('users',[])))
        self.assertEqual(state['roles'],[])
        bad=self.client.post('/api/admin/roles/delete',json={'role_code':'viewer','replacement_role':'sales_rep'})
        self.assertEqual(bad.status_code,403)
        bad=self.client.post('/api/finance/payments/confirm',json={'invoice_id':'INV-101','amount_cents':100,'payment_method':'Cash','reference_number':'ABCD-TEST'})
        self.assertEqual(bad.status_code,403)

    def test_02_client_save_and_stale_detection(self):
        self.login('Ahmed_99')
        data=self.client.get('/api/state').json(); record=dict(data['database']['contacts'][0]);record['id']='C-UNIT-CENTRAL';record['full_name']='عميل اختبار مركزي'
        req={'changes':[{'table':'contacts','op':'insert','id':record['id'],'row':record}]}
        res=self.client.post('/api/changes',json=req)
        self.assertEqual(res.status_code,200,res.text)
        fresh=self.client.get('/api/state').json()
        item=next(r for r in fresh['database']['contacts'] if r['id']==record['id'])
        old_hash=fresh['hashes']['contacts'][record['id']]
        item['full_name']='تحديث على سيرفر المتحدة'
        r=self.client.post('/api/changes',json={'changes':[{'table':'contacts','op':'update','id':record['id'],'row':item,'base_hash':old_hash}]})
        self.assertEqual(r.status_code,200,r.text)
        item['full_name']='تغيير متعارض'
        r=self.client.post('/api/changes',json={'changes':[{'table':'contacts','op':'update','id':record['id'],'row':item,'base_hash':old_hash}]})
        self.assertEqual(r.status_code,409,r.text)

    def test_03_owner_approval_and_sessions(self):
        self.login('Ahmed_99')
        from backend.cloud.app import sessions
        from sqlalchemy import select
        from sqlalchemy.orm import Session
        with Session(self.engine) as con:
            self.assertTrue(con.execute(select(sessions)).first())
        res=self.client.post('/api/admin/roles/delete',json={'role_code':'super_admin'})
        self.assertEqual(res.status_code,400)

    def test_04_finance_payment_idempotency(self):
        c=self.client
        r=c.post('/api/auth/login',json={'username':'finance_nada','password':'StrongTestPass123!'})
        self.assertEqual(r.status_code,200,r.text)
        invoices=c.get('/api/state').json()['database']['invoices']
        inv=next((x for x in invoices if int(x['remaining_cents'])>=125),None)
        self.assertIsNotNone(inv)
        data={'invoice_id':inv['id'],'amount_cents':125,'payment_method':'Bank Transfer','reference_number':'UNIT-TEST-UNIQUE-0001'}
        r=c.post('/api/finance/payments/confirm',json=data)
        self.assertEqual(r.status_code,200,r.text)
        r2=c.post('/api/finance/payments/confirm',json=data)
        self.assertEqual(r2.status_code,409,r2.text)

    def test_05_two_clients_shared_updates(self):
        from fastapi.testclient import TestClient
        from backend.cloud.app import app
        with TestClient(app) as a, TestClient(app) as b:
            self.assertEqual(a.post('/api/auth/login',json={'username':'Ahmed_99','password':'StrongTestPass123!'}).status_code,200)
            self.assertEqual(b.post('/api/auth/login',json={'username':'sales_karim','password':'StrongTestPass123!'}).status_code,200)
            original=a.get('/api/state').json()['database']['contacts'][0].copy()
            original.update(id='C-SECOND-CLIENT',full_name='عميل جديد من جهاز السيلز')
            res=b.post('/api/changes',json={'changes':[{'table':'contacts','op':'insert','id':original['id'],'row':original}]})
            self.assertEqual(res.status_code,200,res.text)
            clients=a.get('/api/state').json()['database']['contacts']
            self.assertTrue(any(x['id']==original['id'] for x in clients))
            self.assertGreaterEqual(a.get('/api/revision').json()['revision'],1)

    def test_06_static_app_and_script(self):
        self.assertEqual(self.client.get('/').status_code,200)
        r=self.client.get('/assets/ues-app.js')
        self.assertEqual(r.status_code,200)
        self.assertIn('centralChanges()',r.text)
        self.assertEqual(self.client.get('/assets/ues.css').status_code,200)

if __name__=='__main__':unittest.main(verbosity=2)
