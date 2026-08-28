#!/usr/bin/env bash
# Re-vendor agent skills from upstream GitHub repos (generated projects).
# Usage: ./scripts/update-skills.sh [--source=<id>]

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYNC_PY="${ROOT_DIR}/scripts/sync_skills.py"
MANIFEST="${ROOT_DIR}/scripts/skills-manifest.json"

if [[ ! -f "${SYNC_PY}" ]]; then
  echo "Error: sync_skills.py not found at ${SYNC_PY}"
  exit 1
fi

if [[ ! -f "${MANIFEST}" ]]; then
  echo "Error: skills-manifest.json not found at ${MANIFEST}"
  exit 1
fi

SOURCE_FILTER=""
for arg in "$@"; do
  case "${arg}" in
    --source=*) SOURCE_FILTER="${arg#--source=}" ;;
  esac
done

ARGS=(--project-root "${ROOT_DIR}" --manifest "${MANIFEST}")
if [[ -n "${SOURCE_FILTER}" ]]; then
  ARGS+=(--source "${SOURCE_FILTER}")
fi

exec python3 "${SYNC_PY}" "${ARGS[@]}"
