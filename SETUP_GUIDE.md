# RiskApp — Setup Guide

## Prerequisites

- Python 3.12+
- Two terminal windows (one for server, one for client)

---

## 1. Open the repository root

From your shell, change into the repository root — the directory that contains `server/`, `client/`, and `qa/`.

If you downloaded a ZIP instead of cloning the repository, extract it first and then `cd` into the extracted project root.

---

## 2. Start the server (Terminal 1)

```bash
cd server
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or requirements.lock for pinned versions
```

Delete any old database (clean start):

```bash
rm -f riskapp.db
```

Start with superadmin auto-creation:

```bash
ALLOW_INSECURE_DEFAULT_SECRET=1 \
INITIAL_SUPERUSER_EMAIL=admin@example.com \
INITIAL_SUPERUSER_PASSWORD='SuperHeslo123!' \
uvicorn riskapp_server.main.app:app --reload
```

On Windows (cmd):

```cmd
set ALLOW_INSECURE_DEFAULT_SECRET=1
set INITIAL_SUPERUSER_EMAIL=admin@example.com
set INITIAL_SUPERUSER_PASSWORD=SuperHeslo123!
uvicorn riskapp_server.main.app:app --reload
```

The server runs on `http://localhost:8000`. At startup it automatically creates the superadmin account.

Verify: `curl http://localhost:8000/health` should return `{"status":"ok","db":"ok"}`.

Leave this terminal running.

---

## 3. Start the client (Terminal 2)

```bash
cd client
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or requirements.lock for pinned versions
```

Delete any old local cache (clean start):

```bash
rm -f ~/.riskapp/client.sqlite3
```

Launch:

```bash
RISKAPP_ALLOW_HTTP=1 python -m riskapp_client.app
```

On Windows (cmd):

```cmd
set RISKAPP_ALLOW_HTTP=1
python -m riskapp_client.app
```

---

## 4. Login dialog

The login dialog has four options:

- **OK** — login to server with email + password
- **Register new account…** — create a new account on the server
- **Work Fully Local (no account, no sync)** — work offline without any account. Data stays on this machine only and will never sync to any server.
- **Cancel** — quit the application

### If server is unreachable after clicking OK:

A **Server Unavailable** dialog appears with:

- **Work Offline as user@example.com (will sync later)** — offline mode with your identity. Data syncs when you restart and server is available. Only appears if you've logged in before or entered credentials.
- **Work Fully Local (no account, no sync)** — anonymous offline, same as above.
- **Quit** — exit.

---

## 5. Login as superadmin

Fill in:

- **Server URL:** `http://localhost:8000`
- **Email:** `admin@example.com`
- **Password:** `SuperHeslo123!`

Click **OK**.

After login the sidebar is empty — no projects are created automatically. Click **"New Project"** to create one.

---

## 6. Register a regular user

Close the client (or open a new instance). Two options:

### Option A: From the client login dialog

1. Launch the client: `RISKAPP_ALLOW_HTTP=1 python -m riskapp_client.app`
2. Click **"Register new account…"**
3. Fill in:
   - **Server URL:** `http://localhost:8000`
   - **Email:** `user@example.com`
   - **Password:** `UserHeslo123!` (min 12 chars, upper + lower + digit + symbol)
   - **Confirm password**
4. Click **OK** — account is created, you are logged in

### Option B: Via curl

```bash
curl -X POST http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"UserHeslo123!"}'
```

Then log in to the client with those credentials.

---

## 7. Add the regular user to a project

1. Login as **superadmin** (`admin@example.com`)
2. Select a project in the sidebar
3. Go to **Members** tab
4. Enter: Email `user@example.com`, Role `member` (or viewer/manager/admin)
5. Click **Add/Update**

The user can now login and see that project.

Note: Superadmin is invisible in the members list when viewed by regular users. Superadmin sees all members including themselves.

---

## 8. Delete a project (superadmin only)

1. Login as **superadmin**
2. Select the project in the sidebar
3. Click **"Delete Project"**
4. Confirm in the warning dialog

This permanently deletes the project and all its data. Regular admins cannot do this.

---

## 9. Offline modes

### Work Fully Local (anonymous)

- No account needed, no server needed
- Data stored in `~/.riskapp/client.sqlite3`
- Projects show `(local only)` suffix in sidebar
- Cannot sync to server — ever
- Isolated: logged-in users cannot see your projects

### Work Offline as user@... (sync later)

- Requires previous login (or entering credentials when server is down)
- Data stored locally with your identity
- Projects show `(offline — will sync)` suffix in sidebar
- Click **Sync Now** when server is available → project is promoted to server
- If project name already exists on server, a numeric suffix is added (e.g. "Test Project (2)")

### Online with offline fallback

- Normal online login
- All changes saved locally + outbox
- If server goes down mid-session, work continues
- Restart client + Sync Now when server is back

---

## Role hierarchy

| Role | Scope | Permissions |
|------|-------|-------------|
| **superadmin** | global | Everything + delete projects + see all projects |
| **admin** | per project | Manage members, snapshots, edit, delete items |
| **manager** | per project | Snapshots, edit, delete items |
| **member** | per project | Edit risks/opportunities/actions |
| **viewer** | per project | Read-only access |

Superadmin is set via `INITIAL_SUPERUSER_EMAIL` at server startup. Regular admins are assigned per project in the Members tab.

---

## Available tabs

| Tab | Description |
|-----|-------------|
| Risks | Risk register with qualitative scoring (P × I) |
| Opportunities | Opportunity register with qualitative scoring |
| Matrix | Probability × Impact matrix view |
| Top history | Snapshot tracking of top-N items over time |
| Actions | Mitigation / contingency / exploit actions |
| Assessments | Per-user scoring of risks and opportunities |
| Members | Project member and role management (admin only) |
| Help Desk | Per-project support ticket system with offline-first sync for server-backed projects |

---

## Sidebar project labels

| Label | Meaning |
|-------|---------|
| `Project Name  (admin@example.com)` | Server project, shows owner email |
| `Project Name  (offline — will sync)` | Local project with identity, will sync |
| `Project Name  (local only)` | Anonymous local project, never syncs |
| `Project Name` | Server project, owner unknown |

---

## Quick restart (clean slate)

```bash
# Terminal 1 (server) — Ctrl+C to stop, then:
cd server
rm -f riskapp.db
ALLOW_INSECURE_DEFAULT_SECRET=1 \
INITIAL_SUPERUSER_EMAIL=admin@example.com \
INITIAL_SUPERUSER_PASSWORD='SuperHeslo123!' \
uvicorn riskapp_server.main.app:app --reload

# Terminal 2 (client):
cd client
rm -f ~/.riskapp/client.sqlite3
RISKAPP_ALLOW_HTTP=1 python -m riskapp_client.app
```

---

## Environment variables reference

### Server

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+pysqlite:///./riskapp.db` | Database connection string |
| `SECRET_KEY` | `change-me` | JWT signing key (MUST set in production) |
| `ALLOW_INSECURE_DEFAULT_SECRET` | (empty) | Set to `1` for local dev |
| `INITIAL_SUPERUSER_EMAIL` | (empty) | Auto-create superadmin at startup |
| `INITIAL_SUPERUSER_PASSWORD` | (empty) | Superadmin password |
| `ACCESS_TOKEN_MINUTES` | `15` | JWT token expiry |
| `REFRESH_TOKEN_DAYS` | `30` | Refresh token expiry |
| `LOGIN_RATE_LIMIT_PER_MINUTE` | `10` | Login attempts per IP+email |
| `MAX_REQUEST_BODY_BYTES` | `2097152` (2MB) | Request body size limit |
| `CORS_ORIGINS` | (empty) | Comma-separated allowed origins |
| `ENFORCE_HTTPS` | `0` | Set to `1` in production |
| `PASSWORD_RESET_RETURN_TOKEN` | (empty) | Set to `1` for dev (returns reset token in response) |

### Client

| Variable | Default | Description |
|----------|---------|-------------|
| `RISKAPP_URL` | `http://localhost:8000` | Server URL |
| `RISKAPP_EMAIL` | (empty) | Skip login dialog if set |
| `RISKAPP_PASSWORD` | (empty) | Skip login dialog if set |
| `RISKAPP_LOCAL_DB` | `~/.riskapp/client.sqlite3` | Local SQLite cache path |
| `RISKAPP_ALLOW_HTTP` | (empty) | Set to `1` to allow plain HTTP |

---

## Password policy

- Minimum 12 characters, maximum 128
- Must include: uppercase letter, lowercase letter, digit, symbol
- Enforced server-side on registration, password reset, and password change
- Example valid password: `SuperHeslo123!`
