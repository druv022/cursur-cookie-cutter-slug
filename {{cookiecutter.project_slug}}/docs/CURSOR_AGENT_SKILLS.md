# Cursor agent skills

This project vendors [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) under `.cursor/skills/` plus two local skills. See `AGENT_SKILLS_VERSION` for the upstream pin.

## Routing

Always-on rule: `.cursor/rules/agent-skills.mdc` → start with `.cursor/skills/using-agent-skills/SKILL.md`, then the phase-matched skill.

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

## Local skills

- **`rtk-token-optimization`** — token-efficient shell via RTK; project hook in `.cursor/hooks.json`.
- **`awesome-agentic-patterns`** — when building agentic apps, fetch latest from https://agentic-patterns.com/llms.txt and cite patterns (do not rely on memory).

## Personas

Optional paste-in personas live under `.cursor/agents/` (not auto-loaded).
