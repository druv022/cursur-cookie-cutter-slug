#!/usr/bin/env bash
# Sync addyosmani/agent-skills into the cookiecutter template project layout.
# Usage: ./scripts/sync-agent-skills.sh [tag-or-ref]
# Wrapper for sync-skills.sh --source=addyosmani-agent-skills

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF="${1:-}"

ARGS=(--source addyosmani-agent-skills)
if [[ -n "${REF}" ]]; then
  echo "Note: ref override via CLI is deprecated; edit scripts/skills-manifest.json ref field."
fi

exec "${ROOT_DIR}/scripts/sync-skills.sh" "${ARGS[@]}"
