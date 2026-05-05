# RiskApp — Test Guide

Complete step-by-step guide for testing all major features.

**Prerequisite:** Server and client are installed and started according to `SETUP_GUIDE.md`.

---

## 1. Clean start

```bash
# Terminal 1 (server):
cd server
source .venv/bin/activate
rm -f riskapp.db

ALLOW_INSECURE_DEFAULT_SECRET=1 \
INITIAL_SUPERUSER_EMAIL=admin@example.com \
INITIAL_SUPERUSER_PASSWORD='SuperHeslo123!' \
uvicorn riskapp_server.main.app:app --reload

# Terminal 2 (client):
cd client
source .venv/bin/activate
rm -f ~/.riskapp/client.sqlite3

RISKAPP_ALLOW_HTTP=1 python -m riskapp_client.app
```

---

## 2. Test: Health check

```bash
curl http://localhost:8000/health
```

**Verify:** `{"status":"ok","db":"ok"}`

---

## 3. Test: Superadmin login + project creation

1. Login dialog → `admin@example.com` / `SuperHeslo123!` → OK
2. **Verify:** Status bar shows `Role: superadmin`
3. **Verify:** Sidebar is empty (no auto-created projects)
4. Click **"New Project"** → name: `Test Project` → OK
5. **Verify:** Sidebar shows `Test Project  (admin@example.com)`

---

## 4. Test: Register a new user

1. Close the client and start it again
2. Click **"Register new account…"**
3. Fill in: `http://localhost:8000`, `user@example.com`, `UserHeslo123!`
4. Confirm
5. **Verify:** "Registration successful" → automatic login
6. **Verify:** Sidebar is empty (the user has no projects yet)

---

## 5. Test: Add user to project

1. Log in as `admin@example.com`
2. Select `Test Project` → **Members** tab
3. Enter `user@example.com`, role `member` → **Add/Update**
4. **Verify:** Table shows `user@example.com` with role `member`
5. **Verify:** Superadmin (`admin@example.com`) sees both themselves and the regular user in the list

---

## 6. Test: Superadmin invisibility

1. Log in as `user@example.com`
2. Select `Test Project` → **Members** tab
3. **Verify:** You see only yourself — the superadmin is not listed
4. **Verify:** Status bar shows `Role: member`

---

## 7. Test: Superadmin protection

A regular user must not be able to change the role of a superadmin:

```bash
LOGIN=$(curl -s -X POST http://localhost:8000/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=UserHeslo123%21')
TOKEN=$(echo "$LOGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

PID=$(curl -s http://localhost:8000/projects \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "import sys,json; ps=[p for p in json.load(sys.stdin) if 'Test' in p['name']]; print(ps[0]['id'])")

curl -s -X POST "http://localhost:8000/projects/$PID/members" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_email":"admin@example.com","role":"viewer"}'
```

**Verify:** `403` — "Only a superadmin can change another superadmin's role"

---

## 8. Test: RBAC — member cannot delete

1. Log in as `user@example.com`
2. `Test Project` → **Risks** tab → **New** → fill in a risk → Save
3. **Verify:** The risk appears, and the status dropdown does not include `deleted` (only managers and above can delete)

---

## 9. Test: Create risks

1. Log in as `admin@example.com`
2. `Test Project` → **Risks** tab → **New**
3. Fill in:
   - Title: `Server outage`
   - Probability: 4, Impact cost: 5, Impact time: 3, Impact scope: 2, Impact quality: 1
   - Description: `Main server outage`
   - Category: `Technical`
   - Status: `active`
4. Save
5. **Verify:** Score = 4 × 5 = 20 (impact = max of the dimension values)
6. Change probability to 2 → Save
7. **Verify:** Score = 2 × 5 = 10

**Note:** The code field is unique per project. A duplicate should trigger an error.

---

## 10. Test: Opportunities

1. Open the **Opportunities** tab → **New**
2. Title: `New market`, Probability: 3, Impact: 4 → Save
3. **Verify:** The button says **"Save Opportunity"** (not "Save Risk")
4. **Verify:** Score = 12

---

## 11. Test: Matrix

1. Open the **Matrix** tab
2. **Verify:** 5×5 table, rows = Probability (1–5), columns = Impact (1–5)
3. The number in each cell = count of risks/opportunities with that P×I combination
4. Switch between `risks` / `opportunities` / `both`

---

## 12. Test: Actions

1. Open the **Actions** tab → **New**
2. Target: risk `Server outage`, Kind: `mitigation`, Title: `Backup server`
3. Save
4. **Verify:** The action appears in the table

---

## 13. Test: Assessments

1. Open the **Risks** tab → select risk `Server outage`
2. Open the **Assessments** tab → P: 2, I: 3, Notes: text → Save
3. **Verify:** Assessment appears in the table, and the Assessor column shows an email address (not a UUID)

---

## 14. Test: Help Desk

1. Open the **Help Desk** tab → **New ticket**
2. Title: `Export does not work`, Category: `bug`, Priority: `high` → Save
3. **Verify:** Ticket appears in the table
4. Select it → change status to `in_progress` → Save
5. Try the filters (Status, Priority)
6. Run **Sync Now** on the current server-backed project
7. Restart the client or pull the project again
8. **Verify:** The ticket is still present with the updated status
9. **Delete** → confirm → ticket disappears
10. Run **Sync Now** again
11. **Verify:** The deleted ticket does not reappear after refresh / restart

**Note:** In server-backed projects, Help Desk tickets participate in offline-first sync. In **Work Fully Local** mode they remain local to the anonymous project.

---

## 15. Test: Work Fully Local

1. Start the client, then click **"Work Fully Local"** in the login dialog
2. **Verify:** App starts and the sidebar contains the bootstrap project `Local Project (local only)`
3. Create a risk and save it
4. Close the client, start it again → **"Work Fully Local"**
5. **Verify:** The risk still exists (data survives restart)
6. Now log in online as `admin@example.com`
7. **Verify:** The local anonymous project is NOT visible — isolation works

---

## 16. Test: Work Offline as user (sync later)

1. Start the client and log in as `admin@example.com` while the server is running
2. Close the client, then **stop the server** (`Ctrl+C`)
3. Start the client again, enter `admin@example.com` + password → OK
4. Server unavailable → **ServerDownDialog** appears
5. Click **"Work Offline as admin@example.com (will sync later)"**
6. **Verify:** Sidebar shows projects with the suffix `(offline — will sync)`
7. Create a new project `Offline Test`, add risks
8. **Start the server again**
9. Close the client, start it, log in online → **Sync Now** on `Offline Test`
10. **Verify:** The project is promoted — the `(offline — will sync)` suffix disappears, and the data is now on the server

---

## 17. Test: Project isolation

1. Log in online and create project `Online A`
2. Click **"Work Fully Local"** in a new session
3. Create project `Local B`
4. **Verify:** The local user does not see `Online A`
5. The online user does not see `Local B`
6. Two separate worlds

---

## 18. Test: Duplicate project name

1. Log in online, create `Test`
2. Try to create another `Test`
3. **Verify:** It is automatically renamed to `Test (2)`
4. Create an offline project `Test`, then promote it while the server already has `Test`
5. **Verify:** It becomes `Test (2)`

---

## 19. Test: Sync and conflict resolution

### Online sync

1. Create risks, click **Sync Now**
2. **Verify:** `ONLINE · pending changes: 0`

### Conflict test (two clients)

```bash
# Terminal 2: Client A
RISKAPP_ALLOW_HTTP=1 python -m riskapp_client.app

# Terminal 3: Client B
RISKAPP_ALLOW_HTTP=1 python -m riskapp_client.app
```

1. **Client A:** Create risk `Conflict Test` → Save → Sync Now
2. **Client B:** Sync Now → risk appears
3. **Client B:** Change title to `Changed by B` → Save → Sync Now
4. **Client A** (without syncing): Change title to `Changed by A` → Save → Sync Now
5. **Client A:** Expected result:
   - Success → last-write-wins, Client A wins (automatic retry)
   - Warning `blocked changes` → retry failed

### Conflict test via curl

```bash
BASE=http://localhost:8000

LOGIN=$(curl -s -X POST "$BASE/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin@example.com&password=SuperHeslo123%21')
TOKEN=$(echo "$LOGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

PID=$(curl -s "$BASE/projects" -H "Authorization: Bearer $TOKEN" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['id'])")

# Create risk (version=1)
RISK=$(curl -s -X POST "$BASE/projects/$PID/risks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Conflict Test","probability":3,"impact":4}')
RID=$(echo "$RISK" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Risk: $RID, version 1"

# Client B updates it (version -> 2)
curl -s -X PATCH "$BASE/projects/$PID/risks/$RID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Changed by B","probability":5}' > /dev/null
echo "Client B -> version 2"

# Client A pushes with stale base_version=1 -> CONFLICT
CID=$(python3 -c "import uuid; print(uuid.uuid4())")
echo "Client A push (stale base_version=1)..."
curl -s -X POST "$BASE/projects/$PID/sync/push" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"project_id\":\"$PID\",\"changes\":[{\"change_id\":\"$CID\",\"entity\":\"risk\",\"op\":\"upsert\",\"base_version\":1,\"record\":{\"id\":\"$RID\",\"title\":\"Changed by A\",\"probability\":1,\"impact\":1}}]}" \
  | python3 -m json.tool
echo "^^^ conflicts: 1, accepted: 0"

# Retry with base_version=2 -> OK
CID2=$(python3 -c "import uuid; print(uuid.uuid4())")
echo "Client A retry (base_version=2)..."
curl -s -X POST "$BASE/projects/$PID/sync/push" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"project_id\":\"$PID\",\"changes\":[{\"change_id\":\"$CID2\",\"entity\":\"risk\",\"op\":\"upsert\",\"base_version\":2,\"record\":{\"id\":\"$RID\",\"title\":\"Changed by A (resolved)\",\"probability\":1,\"impact\":1}}]}" \
  | python3 -m json.tool
echo "^^^ accepted: 1, version now 3"
```

---

## 20. Test: Delete project

1. Log in as superadmin → select project → **"Delete Project"** → confirm
2. **Verify:** Project disappears
3. Log in as regular user → **"Delete Project"**
4. **Verify:** Error `Superadmin privileges required`

---

## 21. Test: Rate limiting

```bash
# Register rate limit (5/min per IP):
for i in $(seq 1 6); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST http://localhost:8000/register \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"test${i}@example.com\",\"password\":\"TestHeslo1234!\"}")
  echo "Attempt $i: HTTP $CODE"
done
# Last one: 429

# Login rate limit (10/min per IP+email):
for i in $(seq 1 11); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST http://localhost:8000/login \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=fake@example.com&password=WrongPassword1')
  echo "Attempt $i: HTTP $CODE"
done
# After 10: 429
```

---

## 22. Test: Request body size limit

```bash
python3 -c "print('{\"email\":\"x@x.com\",\"password\":\"' + 'A'*3000000 + '\"}')" > /tmp/big.json
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -X POST http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -H "Content-Length: $(wc -c < /tmp/big.json)" \
  -d @/tmp/big.json
# Expected: HTTP 413
rm /tmp/big.json
```

---

## 23. Test: Password policy

```bash
# Too short:
curl -s http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"w1@example.com","password":"short"}' | python3 -m json.tool
# 400

# Missing uppercase:
curl -s http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"w2@example.com","password":"nouppercase123!"}' | python3 -m json.tool
# 400

# Valid:
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"valid@example.com","password":"ValidHeslo123!"}'
# 201
```

---

## 24. Test: Top history / snapshots

1. Log in as admin, create several risks
2. Open the **Top history** tab → **Snapshot now**
3. **Verify:** Snapshot appears in the table
4. Change scores, take another snapshot → you should see a trend

**Note:** Snapshots require a synced project (not a local-only one).

---

## 25. Test: CSV export

1. Open the **Risks** tab → **Export CSV**
2. **Verify:** CSV file containing the risk list is created

---

## 26. Automated tests

```bash
cd qa
pip install -r requirements-test.txt
pytest tests/ -v
```

Coverage includes: registration, login, password policy, rate limiting, RBAC, refresh tokens, sync push/pull, conflict detection, assessments, search escaping, password reset, SQLite migrations, outbox queue.
