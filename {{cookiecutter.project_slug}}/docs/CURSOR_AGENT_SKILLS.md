# Cursor agent skills

This project vendors [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) under `.cursor/skills/` plus local skills. See `AGENT_SKILLS_VERSION` for the upstream pin.

[Ponytail](https://github.com/DietrichGebert/ponytail) (lazy senior dev / YAGNI mode) ships as an always-on rule (`.cursor/rules/ponytail.mdc`), six skills, and slash commands. See `PONYTAIL_VERSION` for the upstream pin.

## Routing

Always-on rules: `.cursor/rules/agent-skills.mdc` (skill router) and `.cursor/rules/ponytail.mdc` (minimal implementation). Start lifecycle work with `.cursor/skills/using-agent-skills/SKILL.md`, then the phase-matched skill.

## Lifecycle (slash commands)

| Command | Primary skill(s) |
|---------|------------------|
| `/spec` | `spec-driven-development` |
| `/plan` | `planning-and-task-breakdown` |
| `/build` | `incremental-implementation` + `test-driven-development` |
| `/test` | `test-driven-development` |
| `/review` | `code-review-and-quality` |
| `/code-simplify` | `code-simplification` |
| `/ship` | `shipping-and-launch` |
| `/webperf` | `performance-optimization` |

## Ponytail (minimal implementation)

Always-on: `.cursor/rules/ponytail.mdc` enforces the YAGNI ladder (reuse → stdlib → native → one line → minimum code).

| Command | Skill | Purpose |
|---------|-------|---------|
| `/ponytail` | `ponytail` | Set intensity (`lite` / `full` / `ultra` / `off`) |
| `/ponytail-review` | `ponytail-review` | Review diff for over-engineering; what to delete |
| `/ponytail-audit` | `ponytail-audit` | Repo-wide over-engineering audit |
| `/ponytail-debt` | `ponytail-debt` | Track deferred simplifications |
| `/ponytail-gain` | `ponytail-gain` | Show benchmark impact summary |
| `/ponytail-help` | `ponytail-help` | Command reference |

Use `/review` for correctness, security, and performance. Use `/ponytail-review` when you want a deletion-focused pass. Template unit-test coverage rules still apply alongside ponytail.

## Local skills

- **`rtk-token-optimization`** — token-efficient shell via RTK; project hook in `.cursor/hooks.json`.
- **`awesome-agentic-patterns`** — when building agentic apps, fetch latest from https://agentic-patterns.com/llms.txt and cite patterns (do not rely on memory).
- **`graphify`** — build and query a knowledge graph of the repo (`make graph`, `graphify query`); always-on rule in `.cursor/rules/graphify.mdc`.
- **`ponytail*`** — vendored from DietrichGebert/ponytail; preserved when re-syncing agent-skills.

## Personas

Optional paste-in personas live under `.cursor/agents/` (not auto-loaded).
