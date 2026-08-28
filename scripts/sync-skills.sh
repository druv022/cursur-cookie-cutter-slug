#!/usr/bin/env bash
# Sync all upstream agent skills into the cookiecutter template project layout.
# Usage: ./scripts/sync-skills.sh [--source=<id>]
# Reads scripts/skills-manifest.json

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_FILTER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --source=*) SOURCE_FILTER="${1#--source=}"; shift ;;
    --source)
      SOURCE_FILTER="${2:-}"; shift 2
      ;;
    *) shift ;;
  esac
done

ARGS=(--project-root "${ROOT_DIR}/{{cookiecutter.project_slug}}" --manifest "${ROOT_DIR}/scripts/skills-manifest.json")
if [[ -n "${SOURCE_FILTER}" ]]; then
  ARGS+=(--source "${SOURCE_FILTER}")
fi

exec python3 "${ROOT_DIR}/scripts/sync_skills.py" "${ARGS[@]}"
