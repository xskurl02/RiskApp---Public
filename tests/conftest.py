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


# ---------------------------------------------------------------------------
# Pretty per-test reporter
# ---------------------------------------------------------------------------
# Replaces pytest's default `....F....s` progress with one line per test:
#
#   [ PASS  ]  Refresh endpoint rotates both access and refresh tokens
#   [ FAIL  ]  Login rate limit triggers HTTP 429 after configured failed attempts
#   [ SKIP  ]  ...
#
# The description comes from the test function's first-line docstring and
# falls back to a humanised test id when none is provided.

_COLORS = {
    "PASS": "\033[1;32m",
    "FAIL": "\033[1;31m",
    "ERROR": "\033[1;31m",
    "SKIP": "\033[1;33m",
    "XFAIL": "\033[1;33m",
    "XPASS": "\033[1;33m",
}
_RESET = "\033[0m"


def _resolve_use_color(config: pytest.Config | None) -> bool:
    """Resolve whether to emit ANSI color codes.

    Precedence (highest first):
      1. pytest ``--color=yes|no`` (explicit user choice always wins).
      2. ``FORCE_COLOR`` env var (any non-empty value) → always color.
      3. ``NO_COLOR`` env var (any value) → never color.
      4. ``sys.stdout.isatty()`` for the ``--color=auto`` default.
    """
    if config is not None:
        opt = getattr(config.option, "color", "auto")
        if opt == "yes":
            return True
        if opt == "no":
            return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


_USE_COLOR = True


def _describe_from_doc(doc: str | None) -> str | None:
    if not doc:
        return None
    line = doc.strip().splitlines()[0].strip()
    return line or None


def _humanise_name(name: str) -> str:
    if name.startswith("test_"):
        name = name[len("test_") :]
    return name.replace("_", " ")


def _describe_item(item: pytest.Item) -> str:
    func = getattr(item, "function", None)
    desc = _describe_from_doc(getattr(func, "__doc__", None))
    if desc:
        return desc
    return _humanise_name(item.name)


def _format_line(status: str, description: str) -> str:
    if _USE_COLOR:
        color = _COLORS.get(status, "")
        return f"{color}[ {status:<5} ]{_RESET}  {description}"
    return f"[ {status:<5} ]  {description}"


def pytest_configure(config: pytest.Config) -> None:
    """Switch the built-in terminal reporter into quiet mode.

    Quiet mode disables per-file headers, the per-test ``nodeid PASSED`` line
    that ``-v`` would normally produce, and progress percentages, so the only
    per-test output is the line we print ourselves in
    ``pytest_runtest_logreport``. The session header and final summary line
    are still produced by the built-in reporter.

    This is forced regardless of any user-supplied ``-v``/``-q`` because our
    reporter is meant to fully replace pytest's per-test progress; otherwise
    pytest's verbose nodeid prefix collides with our line and the output
    becomes unreadable.
    """
    config.option.verbose = -1
    global _USE_COLOR
    _USE_COLOR = _resolve_use_color(config)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stash a human-readable description on each report for the log hook."""
    outcome = yield
    report = outcome.get_result()
    report._riskapp_desc = _describe_item(item)


def pytest_report_teststatus(report, config):
    """Suppress pytest's default short letters / verbose words.

    Returning empty short and verbose strings keeps the outcome category
    intact (so the final ``N passed, M failed`` summary is correct) while
    silencing the dot-style progress output we are replacing.
    """
    if report.when == "call":
        return report.outcome, "", ""
    if report.failed:
        return "error", "", ""
    if report.skipped:
        return "skipped", "", ""
    return None


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    description = getattr(report, "_riskapp_desc", None) or report.nodeid

    status: str | None = None
    if report.when == "setup":
        if report.failed:
            status = "ERROR"
        elif report.skipped:
            status = "SKIP"
    elif report.when == "call":
        if report.passed:
            status = "PASS"
        elif report.failed:
            status = "FAIL"
        elif report.skipped:
            status = "SKIP"
    elif report.when == "teardown" and report.failed:
        status = "ERROR"

    if status is None:
        return

    print(_format_line(status, description))


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
