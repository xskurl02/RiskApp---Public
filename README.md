# RiskApp

RiskApp is an offline-first risk and opportunity management app with:

- a FastAPI backend in `server/`;
- a PySide6 desktop client in `client/`;
- test/lint/format tooling in `qa/`;
- setup and development helper scripts in `scripts/`.

## Quick start

From the repository root:

```bash
bash scripts/setup_os_prereqs.sh --desktop
bash scripts/setup_python_env.sh
bash scripts/diagnose_qt_runtime.sh
bash scripts/check_project.sh
```

Start the server:

```bash
RESET_SERVER_DB=1 bash scripts/run_server_dev.sh
```

Start the client in another terminal:

```bash
RESET_CLIENT_DB=1 bash scripts/run_client_dev.sh
```

Login with:

```text
Server URL: http://127.0.0.1:8000
Email: admin@example.com
Password: SuperHeslo123!
```

## Documentation

- [`README_DOCUMENTATION_SECTION.md`](README_DOCUMENTATION_SECTION.md) — documentation index.
- [`SETUP_GUIDE.md`](SETUP_GUIDE.md) — setup and usage.
- [`TEST_GUIDE.md`](TEST_GUIDE.md) — validation checklist.
- [`client/README_CLIENT.md`](client/README_CLIENT.md) — client details.
- [`server/README_SERVER.md`](server/README_SERVER.md) — server details.
- [`qa/README_QA.md`](qa/README_QA.md) — QA/tooling details.
