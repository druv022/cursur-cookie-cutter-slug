#!/usr/bin/env bash
# Explicit user-run installer for RTK (Rust Token Killer) — rtk-ai/rtk.
# Does not mutate ~/.cursor. Project hooks under .cursor/ activate when `rtk` is on PATH.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PINNED="0.43.0"
if [[ -f "${ROOT_DIR}/RTK_VERSION" ]]; then
  PINNED="$(awk -F= '/^version=/{print $2; exit}' "${ROOT_DIR}/RTK_VERSION" || echo "${PINNED}")"
fi

echo "RTK installer (pinned ${PINNED})"
echo "Source: https://github.com/rtk-ai/rtk"
echo ""

if command -v rtk >/dev/null 2>&1 && rtk gain >/dev/null 2>&1; then
  echo "Correct RTK already installed: $(rtk --version 2>/dev/null || echo unknown)"
  rtk gain || true
  echo ""
  echo "Project Cursor hook: .cursor/hooks.json (fail-open)."
  echo "Restart Cursor if hooks were just added."
  exit 0
fi

if command -v rtk >/dev/null 2>&1 && ! rtk gain >/dev/null 2>&1; then
  echo "ERROR: 'rtk' on PATH is not Rust Token Killer (rtk gain failed)."
  echo "You may have Rust Type Kit. Uninstall it, then re-run this script."
  echo "  cargo uninstall rtk   # if installed via cargo"
  exit 1
fi

install_via_brew() {
  brew install rtk
}

install_via_curl() {
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
  if [[ ":${PATH}:" != *":${HOME}/.local/bin:"* ]]; then
    echo ""
    echo "Add to PATH if needed:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
  fi
}

if command -v brew >/dev/null 2>&1; then
  echo "Installing via Homebrew..."
  install_via_brew
elif command -v curl >/dev/null 2>&1; then
  echo "Installing via official install.sh (Homebrew not found)..."
  install_via_curl
else
  echo "ERROR: Need Homebrew or curl to install RTK."
  echo "See https://github.com/rtk-ai/rtk#installation"
  exit 1
fi

echo ""
if ! command -v rtk >/dev/null 2>&1; then
  echo "ERROR: rtk not on PATH after install. Open a new shell and re-check."
  exit 1
fi

if ! rtk gain >/dev/null 2>&1; then
  echo "ERROR: Installed rtk does not support 'rtk gain' (wrong package)."
  exit 1
fi

echo "Installed: $(rtk --version 2>/dev/null || echo rtk)"
echo "Verify savings: rtk gain"
echo ""
echo "Telemetry is opt-in. This script does not enable it."
echo "Project hooks are already in .cursor/hooks.json — restart Cursor to pick them up."
echo "Optional global Cursor init (not required for this project):"
echo "  rtk init -g --agent cursor"
