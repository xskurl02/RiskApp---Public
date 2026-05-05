# RiskApp Desktop Client (PySide6)

Offline-first desktop client for RiskApp.

## Overview

- Local SQLite cache with an outbox
- Manual sync with the server
- Sidebar views for Risks, Opportunities, Matrix, Top history, Actions, Assessments, Members, and Help Desk
- Optional fully local mode for working without an account or server connection

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

From the directory **above** `riskapp_client/`:

```bash
python -m riskapp_client.app
```

## First run

On first launch, the login dialog lets you:

- sign in with an existing account
- register a new account on the server
- work fully local with no account and no sync

You can also create an account directly via the server API:

```bash
curl -X POST http://localhost:8000/register   -H 'Content-Type: application/json'   -d '{"email":"user@example.com","password":"Change-This-Password1!"}'
```

## Configuration (environment variables)

- `RISKAPP_URL` (default: `http://localhost:8000`)
- `RISKAPP_EMAIL` (optional; if missing, a login dialog is shown)
- `RISKAPP_PASSWORD` (optional)
- `RISKAPP_LOCAL_DB` (default: `~/.riskapp/client.sqlite3`)
- `RISKAPP_ALLOW_HTTP` (default: empty)
  - set to `1` only for development if you want to allow `http://` for non-localhost URLs
- `RISKAPP_LOG_LEVEL` (default: `INFO`)

## Notes

- Server-side auth is authoritative.
- Client-side role checks are for UI behavior only.
- Help Desk tickets are stored locally in the client database and, for server-backed projects, participate in the standard offline-first sync flow.
- In **Work Fully Local** mode, Help Desk tickets remain local to the client database, just like the rest of the anonymous local project data.
