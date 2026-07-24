#!/usr/bin/env bash
# Sync addyosmani/agent-skills into the cookiecutter template project layout.
# Usage: ./scripts/sync-agent-skills.sh [tag-or-ref]
# Default pin: 0.6.4 (falls back to main if the tag is missing).

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${ROOT_DIR}/{{cookiecutter.project_slug}}"
PINNED_REF="${1:-0.6.4}"
REPO_URL="https://github.com/addyosmani/agent-skills.git"
TMP_DIR="$(mktemp -d)"
LOCAL_SKILLS=(
  "rtk-token-optimization"
  "awesome-agentic-patterns"
  "graphify"
  "ponytail"
  "ponytail-audit"
  "ponytail-debt"
  "ponytail-gain"
  "ponytail-help"
  "ponytail-review"
)

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "Syncing agent-skills @ ${PINNED_REF} ..."

if ! git clone --depth 1 --branch "${PINNED_REF}" "${REPO_URL}" "${TMP_DIR}/agent-skills" 2>/dev/null; then
  echo "Tag/ref '${PINNED_REF}' not found; falling back to main."
  PINNED_REF="main"
  git clone --depth 1 --branch main "${REPO_URL}" "${TMP_DIR}/agent-skills"
fi

RESOLVED_SHA="$(git -C "${TMP_DIR}/agent-skills" rev-parse HEAD)"
RESOLVED_DESC="$(git -C "${TMP_DIR}/agent-skills" describe --tags --always 2>/dev/null || echo "${RESOLVED_SHA}")"

# Preserve local skills across rsync --delete
BACKUP_DIR="${TMP_DIR}/local-skills-backup"
mkdir -p "${BACKUP_DIR}"
for skill in "${LOCAL_SKILLS[@]}"; do
  if [[ -d "${TEMPLATE_DIR}/.cursor/skills/${skill}" ]]; then
    cp -a "${TEMPLATE_DIR}/.cursor/skills/${skill}" "${BACKUP_DIR}/"
  fi
done

mkdir -p "${TEMPLATE_DIR}/.cursor/skills"
mkdir -p "${TEMPLATE_DIR}/.cursor/agents"
mkdir -p "${TEMPLATE_DIR}/.cursor/commands"
mkdir -p "${TEMPLATE_DIR}/references"

rsync -a --delete \
  --exclude 'rtk-token-optimization/' \
  --exclude 'awesome-agentic-patterns/' \
  --exclude 'graphify/' \
  --exclude 'ponytail/' \
  --exclude 'ponytail-audit/' \
  --exclude 'ponytail-debt/' \
  --exclude 'ponytail-gain/' \
  --exclude 'ponytail-help/' \
  --exclude 'ponytail-review/' \
  "${TMP_DIR}/agent-skills/skills/" \
  "${TEMPLATE_DIR}/.cursor/skills/"

# Restore local skills
for skill in "${LOCAL_SKILLS[@]}"; do
  if [[ -d "${BACKUP_DIR}/${skill}" ]]; then
    rm -rf "${TEMPLATE_DIR}/.cursor/skills/${skill}"
    cp -a "${BACKUP_DIR}/${skill}" "${TEMPLATE_DIR}/.cursor/skills/"
  fi
done

rsync -a --delete \
  "${TMP_DIR}/agent-skills/references/" \
  "${TEMPLATE_DIR}/references/"

rsync -a --delete \
  "${TMP_DIR}/agent-skills/agents/" \
  "${TEMPLATE_DIR}/.cursor/agents/"

# Adapt Claude slash commands → Cursor .cursor/commands/
COMMANDS_SRC="${TMP_DIR}/agent-skills/.claude/commands"
if [[ -d "${COMMANDS_SRC}" ]]; then
  for cmd_file in "${COMMANDS_SRC}"/*.md; do
    [[ -f "${cmd_file}" ]] || continue
    base="$(basename "${cmd_file}")"
    # Rewrite Claude plugin skill references to Cursor project skill paths
    sed -E \
      -e 's/Invoke the agent-skills:([a-z0-9-]+) skill\./Read and follow `.cursor\/skills\/\1\/SKILL.md`./g' \
      -e 's/agent-skills:([a-z0-9-]+)/.cursor\/skills\/\1\/SKILL.md/g' \
      "${cmd_file}" > "${TEMPLATE_DIR}/.cursor/commands/${base}"
  done
fi

cat > "${TEMPLATE_DIR}/AGENT_SKILLS_VERSION" <<EOF
ref=${PINNED_REF}
sha=${RESOLVED_SHA}
describe=${RESOLVED_DESC}
source=${REPO_URL}
synced_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

SKILL_COUNT="$(find "${TEMPLATE_DIR}/.cursor/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
REF_COUNT="$(find "${TEMPLATE_DIR}/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
CMD_COUNT="$(find "${TEMPLATE_DIR}/.cursor/commands" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
AGENT_COUNT="$(find "${TEMPLATE_DIR}/.cursor/agents" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"

echo "Synced agent-skills ${RESOLVED_DESC} (${RESOLVED_SHA})"
echo "  skills:   ${SKILL_COUNT}"
echo "  refs:     ${REF_COUNT}"
echo "  commands: ${CMD_COUNT}"
echo "  agents:   ${AGENT_COUNT}"
echo "Wrote ${TEMPLATE_DIR}/AGENT_SKILLS_VERSION"
