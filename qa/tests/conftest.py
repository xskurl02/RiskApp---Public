from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

# Tests live outside of client/server by design.
# Make both packages importable without requiring editable installs.
ROOT = Path(__file__).resolve().parents[2]
for _p in (ROOT / "server", ROOT / "client"):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)


@pytest.fixture
def isolated_app_factory():
    """Fixture to create an isolated FastAPI app with a clean SQLite DB per test."""

    def _make_app(db_url: str):
        os.environ["DATABASE_URL"] = db_url
        os.environ["AUTO_CREATE_SCHEMA"] = "1"
        os.environ["LOGIN_RATE_LIMIT_PER_MINUTE"] = "2"
        os.environ["LOGIN_RATE_LIMIT_WINDOW_SECONDS"] = "60"
        os.environ["ALLOW_INSECURE_DEFAULT_SECRET"] = "1"

        import riskapp_server.core.config as cfg

        importlib.reload(cfg)
        import riskapp_server.db.session as session

        importlib.reload(session)
        import riskapp_server.auth.service as auth_service

        importlib.reload(auth_service)

        import riskapp_server.core.permissions as permissions

        importlib.reload(permissions)

        import riskapp_server.schemas.models as schemas

        importlib.reload(schemas)

        import riskapp_server.api.routers.crud_factory as crud_factory

        importlib.reload(crud_factory)
        import riskapp_server.api.routers.auth_routes as auth_routes

        importlib.reload(auth_routes)
        import riskapp_server.api.routers.users as users

        importlib.reload(users)
        import riskapp_server.api.routers.projects as projects

        importlib.reload(projects)
        import riskapp_server.api.routers.risks as risks

        importlib.reload(risks)
        import riskapp_server.api.routers.opportunities as opportunities

        importlib.reload(opportunities)
        import riskapp_server.api.routers.items as items

        importlib.reload(items)
        import riskapp_server.api.routers.actions as actions

        importlib.reload(actions)
        import riskapp_server.api.routers.matrix as matrix

        importlib.reload(matrix)
        import riskapp_server.api.routers.snapshots as snapshots

        importlib.reload(snapshots)
        import riskapp_server.api.routers.helpdesk as helpdesk

        importlib.reload(helpdesk)
        import riskapp_server.api.routers.sync_routes as sync_routes

        importlib.reload(sync_routes)

        import riskapp_server.sync.engine as sync_engine

        importlib.reload(sync_engine)

        import riskapp_server.main.app as main_app

        importlib.reload(main_app)

        return main_app.create_app()

    return _make_app
