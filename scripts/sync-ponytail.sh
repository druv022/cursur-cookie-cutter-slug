#!/usr/bin/env bash
# Sync DietrichGebert/ponytail into the cookiecutter template project layout.
# Usage: ./scripts/sync-ponytail.sh [tag-or-ref]
# Default pin: v4.8.4 (falls back to main if the tag is missing).

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${ROOT_DIR}/{{cookiecutter.project_slug}}"
PINNED_REF="${1:-v4.8.4}"
REPO_URL="https://github.com/DietrichGebert/ponytail.git"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "Syncing ponytail @ ${PINNED_REF} ..."

if ! git clone --depth 1 --branch "${PINNED_REF}" "${REPO_URL}" "${TMP_DIR}/ponytail" 2>/dev/null; then
  echo "Tag/ref '${PINNED_REF}' not found; falling back to main."
  PINNED_REF="main"
  git clone --depth 1 --branch main "${REPO_URL}" "${TMP_DIR}/ponytail"
fi

RESOLVED_SHA="$(git -C "${TMP_DIR}/ponytail" rev-parse HEAD)"
RESOLVED_DESC="$(git -C "${TMP_DIR}/ponytail" describe --tags --always 2>/dev/null || echo "${RESOLVED_SHA}")"

mkdir -p "${TEMPLATE_DIR}/.cursor/rules"
mkdir -p "${TEMPLATE_DIR}/.cursor/skills"
mkdir -p "${TEMPLATE_DIR}/.cursor/commands"

cp "${TMP_DIR}/ponytail/.cursor/rules/ponytail.mdc" \
  "${TEMPLATE_DIR}/.cursor/rules/ponytail.mdc"

for skill_dir in "${TMP_DIR}/ponytail"/skills/ponytail*; do
  [[ -d "${skill_dir}" ]] || continue
  skill_name="$(basename "${skill_dir}")"
  rm -rf "${TEMPLATE_DIR}/.cursor/skills/${skill_name}"
  cp -a "${skill_dir}" "${TEMPLATE_DIR}/.cursor/skills/${skill_name}"
done

# Adapt ponytail TOML slash commands → Cursor .cursor/commands/*.md
toml_to_cursor_cmd() {
  local toml_file="$1"
  local out_file="$2"
  local description prompt
  description="$(awk -F'"' '/^description = / { print $2; exit }' "${toml_file}")"
  prompt="$(awk -F'"' '/^prompt = / { print $2; exit }' "${toml_file}")"
  # Upstream plugin prompts use {{args}}; escape for cookiecutter Jinja2 rendering.
  prompt="${prompt//\{\{args\}\}/the level the user provided (lite, full, ultra, or off)}"
  {
    echo "---"
    echo "description: ${description}"
    echo "---"
    echo ""
    local base
    base="$(basename "${toml_file}" .toml)"
    if [[ "${base}" == "ponytail" ]]; then
      echo "Read and follow \`.cursor/skills/ponytail/SKILL.md\`."
      echo ""
    else
      echo "Read and follow \`.cursor/skills/${base}/SKILL.md\`."
      echo ""
    fi
    echo "${prompt}"
  } > "${out_file}"
}

for toml_file in "${TMP_DIR}/ponytail"/commands/*.toml; do
  [[ -f "${toml_file}" ]] || continue
  base="$(basename "${toml_file}" .toml)"
  toml_to_cursor_cmd "${toml_file}" "${TEMPLATE_DIR}/.cursor/commands/${base}.md"
done

cat > "${TEMPLATE_DIR}/PONYTAIL_VERSION" <<EOF
ref=${PINNED_REF}
sha=${RESOLVED_SHA}
describe=${RESOLVED_DESC}
source=${REPO_URL}
synced_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

RULE_COUNT="$(find "${TEMPLATE_DIR}/.cursor/rules" -maxdepth 1 -name 'ponytail.mdc' | wc -l | tr -d ' ')"
SKILL_COUNT="$(find "${TEMPLATE_DIR}/.cursor/skills" -mindepth 1 -maxdepth 1 -type d -name 'ponytail*' | wc -l | tr -d ' ')"
CMD_COUNT="$(find "${TEMPLATE_DIR}/.cursor/commands" -maxdepth 1 -type f -name 'ponytail*.md' | wc -l | tr -d ' ')"

echo "Synced ponytail ${RESOLVED_DESC} (${RESOLVED_SHA})"
echo "  rule:     ${RULE_COUNT}"
echo "  skills:   ${SKILL_COUNT}"
echo "  commands: ${CMD_COUNT}"
echo "Wrote ${TEMPLATE_DIR}/PONYTAIL_VERSION"
