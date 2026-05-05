# RiskApp Server (FastAPI)

FastAPI backend for the RiskApp project.

## Overview

- Risks and opportunities CRUD
- Actions and assessments
- Matrix, snapshot, and Help Desk endpoints
- Offline sync for risks, opportunities, actions, assessments, and Help Desk tickets
- JWT auth and role checks

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

From the directory **above** `riskapp_server/`:

```bash
# Development server
uvicorn riskapp_server.main.app:app --reload

# Development convenience entry point
python -m riskapp_server
```

> `python -m riskapp_server` currently starts Uvicorn with `reload=True`, so it should be treated as a development entry point rather than a production launcher.

## First run (create a user)

Use the registration endpoint to create the first user.

```bash
curl -X POST http://localhost:8000/register   -H 'Content-Type: application/json'   -d '{"email":"admin@example.com","password":"Change-This-Password1!"}'
```

Then log in:

```bash
curl -X POST http://localhost:8000/login   -H 'Content-Type: application/x-www-form-urlencoded'   -d 'username=admin@example.com&password=Change-This-Password1!'
```

## Help Desk endpoints

The server exposes Help Desk CRUD routes per project:

- `GET /projects/{project_id}/helpdesk/tickets`
- `POST /projects/{project_id}/helpdesk/tickets`
- `PATCH /projects/{project_id}/helpdesk/tickets/{ticket_id}`
- `DELETE /projects/{project_id}/helpdesk/tickets/{ticket_id}`

Help Desk tickets are also included in the sync push/pull pipeline for server-backed projects.

## Configuration (environment variables)

Common settings:

- `DATABASE_URL` (default: `sqlite+pysqlite:///./riskapp.db`)
- `ENV` (default: `development`; set `production` in deployments)
- `SECRET_KEY` (default: `change-me`)
  - **Required in production** unless you explicitly set `ALLOW_INSECURE_DEFAULT_SECRET=1`
- `ACCESS_TOKEN_MINUTES` (default: `15`) *(legacy alias: `TOKEN_MINUTES`)*
- `REFRESH_TOKEN_DAYS` (default: `30`)
- `AUTO_CREATE_SCHEMA` (default: `1`)
  - set to `0` in production if you manage schema with migrations
- `ENFORCE_HTTPS` (enabled automatically in production unless overridden)
- `TRUST_X_FORWARDED_PROTO` (defaults to `1` in production, `0` otherwise)
- `INITIAL_SUPERUSER_EMAIL` (optional)
- `INITIAL_SUPERUSER_PASSWORD` (optional)
- `CORS_ORIGINS` (comma-separated list; optional)

Sync settings:

- `MAX_SYNC_PULL_PER_ENTITY` (default: `5000`)
- `SYNC_PUSH_EXUNGE_EVERY` (default: `200`)

## Notes

- Probability and impact use a `1..5` scale.
- Score is `probability * impact`.
- If per-dimension impacts are present, the effective `impact` is recalculated from the maximum of the provided impact dimensions.
