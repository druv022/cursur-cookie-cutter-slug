---
name: rtk-token-optimization
description: >-
  Uses RTK (Rust Token Killer) to compress verbose shell command output before
  it reaches LLM context. Use when running git, pytest, uv, ruff, docker,
  package managers, or other high-volume CLI commands in an agent session.
---

# RTK Token Optimization

## Overview

[RTK](https://github.com/rtk-ai/rtk) filters and compresses command outputs (often 60–90% fewer tokens). This project includes a fail-open Cursor `preToolUse` hook that rewrites Shell commands to `rtk …` when the binary is available.

## When to Use

- Running tests (`pytest`, `uv run pytest`)
- Linting (`ruff check`)
- Git status/diff/log/add/commit/push
- Docker / compose listings and logs
- Any shell command whose raw output is large and noisy

**When NOT required:** Tiny one-line checks where output is already compact, or when the user sets `RTK_DISABLED=1`.

## Verify the Correct Binary

There are two unrelated projects named `rtk`. Always confirm:

```bash
rtk --version
rtk gain   # MUST show token savings stats — not "command not found"
```

If `rtk gain` fails, you have the wrong package (Rust Type Kit). Direct the user to `scripts/install-rtk.sh` or Homebrew `brew install rtk` from [rtk-ai/rtk](https://github.com/rtk-ai/rtk).

## Preferred Commands (this template)

| Task | Prefer |
|------|--------|
| Tests | `rtk pytest` or `rtk uv run pytest` |
| Lint | `rtk ruff check` |
| Git status | `rtk git status` |
| Git diff | `rtk git diff` |
| Docker | `rtk docker ps` / `rtk docker compose ps` |
| Generic failures-only | `rtk test <cmd>` / `rtk err <cmd>` |

If the Cursor hook is active, plain `git status` / `pytest` may already be rewritten — do not double-prefix with `rtk`.

## Overrides

```bash
RTK_DISABLED=1 git status   # bypass rewrite for one command
```

## Failure Recovery

When a command fails, RTK may truncate success noise but save full output under a path like `~/.local/share/rtk/tee/…`. **If compressed failure output is insufficient, read that full log** before guessing about the error.

## Installation (user action)

Do not silently download binaries. Point the user at:

```bash
./scripts/install-rtk.sh
# then restart Cursor so the project hook can resolve `rtk`
```

Pinned version is recorded in `RTK_VERSION`. Telemetry stays disabled unless the user opts in separately.

## Verification

- [ ] `rtk gain` works (correct binary)
- [ ] Verbose commands return compact output (or hook rewrote them)
- [ ] On failure, full tee path was consulted when needed
- [ ] `RTK_DISABLED=1` still allows raw commands
