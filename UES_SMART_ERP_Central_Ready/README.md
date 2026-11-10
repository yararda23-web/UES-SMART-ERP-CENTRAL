# UES Smart ERP Central Edition v3.0.0

**Status:** Deployable central architecture / staging build — not yet a validated production ERP.

This is a modified version of UES Smart ERP v2.5.2, preserving its Arabic UI and turning the Desktop EXE into a client of a single HTTPS API. New central backend uses Python FastAPI + SQLAlchemy/PostgreSQL, with database sessions, server-side permissions, per-record changes with conflict detection, one-authority finance payment confirmation, revision polling, and optional WebSocket notification. It no longer runs Python or copies SQLite on employee PCs.

## Main folders

- `backend/cloud/app.py`: central API server, authentication, RBAC, finance, state and synchronization.
- `database/schema.sql`: base relational database schema; initialized automatically if no business tables exist.
- `frontend/src/`: Arabic application source; `frontend/dist/`: built web app.
- `electron/main.js`, `electron/setup.html`: Windows desktop client; asks for HTTPS server URL at first launch.
- `scripts/migrate_sqlite_to_postgres.py`: non-destructive inspection, explicit one-time import.
- `deployment/Dockerfile` / `railway.json`: cloud deployment configs.
- `docker-compose.yml`: optional local PostgreSQL test.
- `tests/test_central_api.py`: isolated API security / persistence tests.
- `docs/legacy/`: old local build scripts, retained **for reference only**. Do not run them for the central version.

## Start central server locally (test only)

Requires Python 3.12+.

```bash
python -m pip install -r backend/cloud/requirements.txt
# On Windows PowerShell:
$env:DATABASE_URL="sqlite:///C:/temp/ues-central-test.db"
$env:UES_PUBLIC_URL="http://127.0.0.1:8000"
$env:UES_ALLOWED_HOSTS="127.0.0.1,localhost"
python -m uvicorn backend.cloud.app:app --host 127.0.0.1 --port 8000
```

Test DB starts EMPTY and has no accounts; to log in, import a **demo copy** following START_HERE_AR.md, or use the PostgreSQL migration utility. Never use original demo credentials with live client data.

## Railway production-target configuration

1. Deploy `deployment/Dockerfile` from a **private repository**.
2. Add Railway PostgreSQL to the same project.
3. Set app service `DATABASE_URL` to the database service reference (never expose it to frontend/client).
4. Set `UES_PUBLIC_URL=https://YOUR-UES-DOMAIN` and `UES_ALLOWED_HOSTS=YOUR-UES-DOMAIN`.
5. Healthcheck `/api/health` should report `UES-SMART-ERP-CENTRAL`.
6. Backups and a domain/TLS validation must be configured before real data.
7. Import existing local SQLite **once** into the EMPTY PostgreSQL database, with password reset for Owner and deactivated other accounts.

The server does not provide live OpenAI/WhatsApp/etc. integrations; those remain disconnected simulations. Do not place API keys in the EXE or UI.

## Windows installer

Run `BUILD_CENTRAL_WINDOWS_EXE.bat` after installing Node.js LTS. On Windows, electron-builder can create `release/UES-Smart-ERP-Central-Setup-3.0.0.exe`. The EXE is a thin client: no Python installation, no independent SQLite. It opens a secure setup form on first launch asking for the UES server HTTPS URL.

## Limits and open work

- No remote PostgreSQL or cloud Railway service has been provisioned by this package. Live deployment requires the owner's cloud account and credentials.
- Core generic forms use row-level diff saves, not yet dedicated validated endpoints for every quote/contract/project workflow. Review these flows before commercial deployment.
- WebSocket notifications are in-process, designed for a single API worker; 7-second revision polling is the recovery/fallback. Multiple servers should use Redis/Postgres pub-sub.
- External WhatsApp, Facebook, Instagram, Telegram, payment gateways and live OpenAI calls are **not** connected.
- Hosted production databases require scheduled backups, TLS review, credential rotation, secrets manager, external security audit and authenticated production smoke tests.
- No Windows EXE was compiled or signed in this Linux evaluation environment.

Read `START_HERE_AR.md` for detailed Arabic steps and migration safeguards; see `docs/CENTRAL_QA_AR.md` for verified tests and known gaps.
