"""Environment-backed application settings."""

from __future__ import annotations

import os

ENV: str = os.getenv("ENV", "development").strip().lower()

SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")

# Allow the default key for local runs. Set a real secret in deployments.
ALLOW_INSECURE_DEFAULT_SECRET: bool = (
    os.getenv("ALLOW_INSECURE_DEFAULT_SECRET", "").strip() == "1"
)
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
TOKEN_MINUTES: int = int(os.getenv("TOKEN_MINUTES", "15"))

# ACCESS_TOKEN_MINUTES falls back to TOKEN_MINUTES.
ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES", str(TOKEN_MINUTES)))
REFRESH_TOKEN_DAYS: int = int(os.getenv("REFRESH_TOKEN_DAYS", "30"))

# Local in-process limiter for /login.
LOGIN_RATE_LIMIT_PER_MINUTE: int = int(os.getenv("LOGIN_RATE_LIMIT_PER_MINUTE", "10"))
LOGIN_RATE_LIMIT_WINDOW_SECONDS: int = int(
    os.getenv("LOGIN_RATE_LIMIT_WINDOW_SECONDS", "60")
)

PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", "12"))
PASSWORD_MAX_LENGTH: int = int(os.getenv("PASSWORD_MAX_LENGTH", "128"))
PASSWORD_REQUIRE_UPPER: bool = os.getenv("PASSWORD_REQUIRE_UPPER", "1").strip() not in {
    "0",
    "false",
    "False",
}
PASSWORD_REQUIRE_LOWER: bool = os.getenv("PASSWORD_REQUIRE_LOWER", "1").strip() not in {
    "0",
    "false",
    "False",
}
PASSWORD_REQUIRE_DIGIT: bool = os.getenv("PASSWORD_REQUIRE_DIGIT", "1").strip() not in {
    "0",
    "false",
    "False",
}
PASSWORD_REQUIRE_SYMBOL: bool = os.getenv(
    "PASSWORD_REQUIRE_SYMBOL", "1"
).strip() not in {"0", "false", "False"}

PASSWORD_RESET_TOKEN_MINUTES: int = int(os.getenv("PASSWORD_RESET_TOKEN_MINUTES", "15"))

# Tests and local runs can return the reset token directly.
PASSWORD_RESET_RETURN_TOKEN: bool = (
    os.getenv("PASSWORD_RESET_RETURN_TOKEN", "").strip() == "1"
)

ENFORCE_HTTPS: bool = (
    os.getenv("ENFORCE_HTTPS", "").strip() == "1" or ENV == "production"
)
TRUST_X_FORWARDED_PROTO: bool = os.getenv(
    "TRUST_X_FORWARDED_PROTO", "1" if ENV == "production" else "0"
).strip() not in {"0", "false", "False"}

# Create a superuser at startup when these are set.
INITIAL_SUPERUSER_EMAIL: str | None = os.getenv("INITIAL_SUPERUSER_EMAIL")
INITIAL_SUPERUSER_PASSWORD: str | None = os.getenv("INITIAL_SUPERUSER_PASSWORD")

PBKDF2_ITERS: int = int(os.getenv("PBKDF2_ITERS", "200000"))

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite+pysqlite:///./riskapp.db",
)

DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))  # seconds; 0 disables
DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

DB_STATEMENT_TIMEOUT_MS: int = int(os.getenv("DB_STATEMENT_TIMEOUT_MS", "30000"))

GZIP_ENABLED: bool = os.getenv("GZIP_ENABLED", "1").strip() not in {
    "0",
    "false",
    "False",
}
GZIP_MINIMUM_SIZE: int = int(os.getenv("GZIP_MINIMUM_SIZE", "1024"))

# Disable this if you manage schema with migrations.
AUTO_CREATE_SCHEMA: bool = os.getenv("AUTO_CREATE_SCHEMA", "1").strip() not in {
    "0",
    "false",
    "False",
}

# Cap results for non-paginated sync pulls.
MAX_SYNC_PULL_PER_ENTITY: int = int(os.getenv("MAX_SYNC_PULL_PER_ENTITY", "5000"))

# Flush and expunge periodically during sync push.
SYNC_PUSH_EXUNGE_EVERY: int = int(os.getenv("SYNC_PUSH_EXUNGE_EVERY", "200"))

SNAPSHOT_INSERT_CHUNK: int = int(os.getenv("SNAPSHOT_INSERT_CHUNK", "1000"))

RETENTION_DAYS: int = int(os.getenv("RETENTION_DAYS", "180"))

CORS_ORIGINS: list[str] = [
    o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()
]
