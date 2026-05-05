#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  echo "ERROR: Missing .venv. Run scripts/setup_py314_env.sh first."
  exit 1
fi

source .venv/bin/activate

case "${1:-}" in
  --fix)
    echo "Running Ruff autofix..."
    ruff check --config qa/pyproject.toml . --fix
    ;;
  "")
    ;;
  *)
    echo "Usage: $0 [--fix]"
    exit 2
    ;;
esac

echo "Running tests..."
bash qa/scripts/test.sh

echo "Running lint..."
bash qa/scripts/lint.sh

echo "Running pip check..."
python -m pip check

echo "All checks passed."