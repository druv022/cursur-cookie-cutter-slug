#!/usr/bin/env bash
# Re-apply the cookiecutter template to this project (overwrite template files).
#
# Usage:
#   COOKIECUTTER_TEMPLATE=/path/to/cursur-cookie-cutter-slug ./scripts/update-from-template.sh
#   ./scripts/update-from-template.sh /path/to/cursur-cookie-cutter-slug

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="${1:-${COOKIECUTTER_TEMPLATE:-}}"

if [[ -z "$TEMPLATE" ]]; then
    cat <<'EOF'
Set COOKIECUTTER_TEMPLATE or pass the template path as the first argument.

Example:
  COOKIECUTTER_TEMPLATE=~/Codes/cookie-cutter/cursur-cookie-cutter-slug ./scripts/update-from-template.sh
EOF
    exit 1
fi

TEMPLATE="$(cd "$TEMPLATE" && pwd)"
PARENT_DIR="$(dirname "$PROJECT_ROOT")"
PROJECT_SLUG="$(basename "$PROJECT_ROOT")"

echo "Refreshing ${PROJECT_SLUG} from ${TEMPLATE} ..."
exec cookiecutter "$TEMPLATE" -o "$PARENT_DIR" -f --replay
