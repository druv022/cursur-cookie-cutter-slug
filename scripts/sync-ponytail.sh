#!/usr/bin/env bash
# Sync DietrichGebert/ponytail into the cookiecutter template project layout.
# Usage: ./scripts/sync-ponytail.sh [tag-or-ref]
# Wrapper for sync-skills.sh --source=ponytail

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF="${1:-}"

ARGS=(--source ponytail)
if [[ -n "${REF}" ]]; then
  echo "Note: ref override via CLI is deprecated; edit scripts/skills-manifest.json ref field."
fi

exec "${ROOT_DIR}/scripts/sync-skills.sh" "${ARGS[@]}"
