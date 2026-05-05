#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

MODE="--desktop"
SKIP_APT=0
DO_RELOCK=0
DO_FIX=0
RESET_STATE=0

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/one_shot_clean_setup.sh [options]

Options:
  --desktop         Use desktop prerequisites. Default.
  --server-only     Use server-only prerequisites.
  --headless-gui    Use headless GUI prerequisites.
  --all             Use all prerequisites.

  --skip-apt        Do not run setup_ubuntu_prereqs.sh.
  --relock          Run relock_py314.sh before environment setup.
  --fix             Run check_project.sh --fix.
  --reset-state     Run reset_dev_state.sh --yes at the end.

Examples:
  bash scripts/one_shot_clean_setup.sh
  bash scripts/one_shot_clean_setup.sh --skip-apt
  bash scripts/one_shot_clean_setup.sh --relock
  bash scripts/one_shot_clean_setup.sh --fix
  bash scripts/one_shot_clean_setup.sh --all --relock --fix
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --desktop|--server-only|--headless-gui|--all)
      MODE="$1"
      shift
      ;;
    --skip-apt)
      SKIP_APT=1
      shift
      ;;
    --relock)
      DO_RELOCK=1
      shift
      ;;
    --fix)
      DO_FIX=1
      shift
      ;;
    --reset-state)
      RESET_STATE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 2
      ;;
  esac
done

run_step() {
  local title="$1"
  shift

  echo
  echo "==> $title"
  "$@"
}

if [[ "$SKIP_APT" -eq 0 ]]; then
  run_step "Installing Ubuntu prerequisites" \
    bash scripts/setup_ubuntu_prereqs.sh "$MODE"
fi

if [[ "$DO_RELOCK" -eq 1 ]]; then
  run_step "Regenerating Python 3.14 lock files" \
    bash scripts/relock_py314.sh
fi

run_step "Creating Python 3.14 environment" \
  bash scripts/setup_py314_env.sh

if [[ "$DO_FIX" -eq 1 ]]; then
  run_step "Running tests/lint with Ruff autofix" \
    bash scripts/check_project.sh --fix
else
  run_step "Running tests/lint" \
    bash scripts/check_project.sh
fi

if [[ "$RESET_STATE" -eq 1 ]]; then
  run_step "Resetting dev state" \
    bash scripts/reset_dev_state.sh --yes
fi

echo
echo "Done."
echo
echo "Start server:"
echo "  RESET_SERVER_DB=1 bash scripts/run_server_dev.sh"
echo
echo "Start client:"
echo "  RESET_CLIENT_DB=1 bash scripts/run_client_dev.sh"