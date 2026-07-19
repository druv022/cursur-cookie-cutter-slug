#!/usr/bin/env bash
# Fail-open Cursor preToolUse hook: rewrite Shell commands through RTK when available.
# If RTK is missing, wrong package, or rewrite fails, pass through unchanged.

set -u

# Always allow the tool if anything goes wrong.
passthrough() {
  exit 0
}

if [[ -n "${RTK_DISABLED:-}" ]]; then
  passthrough
fi

if ! command -v rtk >/dev/null 2>&1; then
  passthrough
fi

# Confirm Token Killer (not Rust Type Kit)
if ! rtk gain >/dev/null 2>&1; then
  echo "[rtk] WARNING: rtk on PATH is not Rust Token Killer (rtk gain failed); skipping rewrite" >&2
  passthrough
fi

INPUT="$(cat || true)"
if [[ -z "${INPUT}" ]]; then
  passthrough
fi

# Prefer python3 for JSON; fall back to jq; else pass through.
extract_cmd() {
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "${INPUT}" | python3 -c 'import json,sys
try:
  d=json.load(sys.stdin)
  print((d.get("tool_input") or {}).get("command") or d.get("command") or "")
except Exception:
  print("")
'
  elif command -v jq >/dev/null 2>&1; then
    printf '%s' "${INPUT}" | jq -r '.tool_input.command // .command // empty'
  else
    echo ""
  fi
}

CMD="$(extract_cmd)"
if [[ -z "${CMD}" ]]; then
  passthrough
fi

# Already using rtk
case "${CMD}" in
  rtk\ *|*/rtk\ *) passthrough ;;
esac

REWRITTEN="$(rtk rewrite "${CMD}" 2>/dev/null || true)"
if [[ -z "${REWRITTEN}" || "${REWRITTEN}" == "${CMD}" ]]; then
  passthrough
fi

emit_updated() {
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "${INPUT}" | python3 -c 'import json,sys
raw=sys.stdin.read()
cmd=sys.argv[1]
try:
  d=json.loads(raw)
except Exception:
  sys.exit(0)
ti=dict(d.get("tool_input") or {})
if "command" in ti or "tool_input" in d:
  ti["command"]=cmd
  out={"permission":"allow","updated_input":ti}
else:
  out={"permission":"allow","updated_input":{"command":cmd}}
print(json.dumps(out))
' "${REWRITTEN}"
  elif command -v jq >/dev/null 2>&1; then
    printf '%s' "${INPUT}" | jq -c --arg cmd "${REWRITTEN}" '
      if .tool_input then
        {permission:"allow", updated_input:(.tool_input | .command=$cmd)}
      else
        {permission:"allow", updated_input:{command:$cmd}}
      end
    '
  else
    passthrough
  fi
}

emit_updated
exit 0
