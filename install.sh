#!/usr/bin/env bash
# Install or check the kit.  Usage:  bash install.sh   |   bash install.sh --check
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is needed (the installer and the kit's guard hook both use it)."
  echo "On a Mac, run:  xcode-select --install   and then run this again."
  exit 1
fi
exec python3 scripts/install.py "$@"
