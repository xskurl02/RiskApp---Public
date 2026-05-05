#!/usr/bin/env bash
set -euo pipefail

MODE="${1:---desktop}"

if ! command -v apt >/dev/null 2>&1; then
  echo "ERROR: This script expects Ubuntu/Debian with apt."
  exit 1
fi

sudo apt update

sudo apt install -y \
  ca-certificates \
  curl \
  unzip \
  git \
  sqlite3 \
  build-essential \
  python3 \
  python3-venv \
  python3-pip \
  python3-dev

install_gui_packages() {
  sudo apt install -y \
    libegl1 \
    libgl1 \
    libfontconfig1 \
    libxkbcommon-x11-0 \
    libxcb1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0
}

case "$MODE" in
  --server-only)
    ;;
  --desktop)
    install_gui_packages
    ;;
  --headless-gui)
    sudo apt install -y xvfb dbus-x11
    install_gui_packages
    ;;
  --all)
    sudo apt install -y xvfb dbus-x11 libreoffice-calc
    install_gui_packages
    ;;
  *)
    echo "Usage: $0 [--server-only|--desktop|--headless-gui|--all]"
    exit 2
    ;;
esac

echo "Ubuntu prerequisites installed for mode: $MODE"