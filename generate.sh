#!/usr/bin/env bash
# Create a new project or refresh an existing one from this cookiecutter template.
#
# Usage:
#   ./generate.sh [cookiecutter options and extra_context key=value ...]
#   ./generate.sh -o /path/to/parent-dir
#   ./generate.sh --update          # force update mode (-f --replay)
#
# Update mode (-f --overwrite-if-exists) is enabled automatically when a replay
# file exists and the matching project directory is already present under -o.

set -euo pipefail

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_NAME="$(basename "$TEMPLATE_DIR")"
OUTPUT_DIR="."
FORCE_UPDATE=false
USER_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output-dir)
            OUTPUT_DIR="$2"
            USER_ARGS+=("$1" "$2")
            shift 2
            ;;
        -u|--update)
            FORCE_UPDATE=true
            shift
            ;;
        -h|--help)
            cat <<'EOF'
Usage: ./generate.sh [options] [key=value ...]

Create a new project or update an existing one from this cookiecutter template.

Options:
  -o, --output-dir DIR   Parent directory for the generated project (default: .)
  -u, --update           Update mode: overwrite template files and reuse last prompts
  -h, --help             Show this help

When a project directory already exists, this script passes --overwrite-if-exists
to cookiecutter so template files are refreshed instead of failing.

If ~/.cookiecutter_replay/<template>.json exists and matches an existing project
folder, --replay is also used so you are not re-prompted.

Examples:
  ./generate.sh
  ./generate.sh -o ~/projects
  ./generate.sh --update -o ~/projects
  ./generate.sh project_slug=my_app -o .
EOF
            exit 0
            ;;
        *)
            USER_ARGS+=("$1")
            shift
            ;;
    esac
done

OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"
REPLAY_FILE="${HOME}/.cookiecutter_replay/${TEMPLATE_NAME}.json"
UPDATE_MODE=false
PROJECT_SLUG=""

if [[ "$FORCE_UPDATE" == true ]]; then
    UPDATE_MODE=true
elif [[ -f "$REPLAY_FILE" ]]; then
    PROJECT_SLUG="$(
        python3 - <<'PY' "$REPLAY_FILE"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)
print(data["cookiecutter"]["project_slug"])
PY
    )"
    if [[ -n "$PROJECT_SLUG" && -d "${OUTPUT_DIR}/${PROJECT_SLUG}" ]]; then
        UPDATE_MODE=true
    fi
fi

HAS_NO_INPUT=false
HAS_EXTRA_CONTEXT=false
for arg in "${USER_ARGS[@]}"; do
    if [[ "$arg" == "--no-input" ]]; then
        HAS_NO_INPUT=true
    elif [[ "$arg" == *=* ]]; then
        HAS_EXTRA_CONTEXT=true
    fi
done

COOKIE_ARGS=(-o "$OUTPUT_DIR" -f)
if [[ "$UPDATE_MODE" == true ]]; then
    if [[ "$HAS_NO_INPUT" == false && "$HAS_EXTRA_CONTEXT" == false ]]; then
        COOKIE_ARGS+=(--replay)
    fi
    if [[ -n "$PROJECT_SLUG" ]]; then
        echo "Updating existing project at ${OUTPUT_DIR}/${PROJECT_SLUG} ..."
    else
        echo "Updating existing project ..."
    fi
else
    echo "Generating project into ${OUTPUT_DIR} ..."
fi

exec cookiecutter "$TEMPLATE_DIR" "${COOKIE_ARGS[@]}" "${USER_ARGS[@]}"
