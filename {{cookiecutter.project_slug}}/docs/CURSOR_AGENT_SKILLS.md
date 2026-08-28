# Cursor agent skills

This project vendors a **curated multi-upstream skills bundle** under `.cursor/skills/`. Pins and SHAs live in `SKILLS_LOCK.json` (legacy: `AGENT_SKILLS_VERSION`, `PONYTAIL_VERSION`).

To refresh from upstream: `./scripts/update-skills.sh`, `make update-skills`, or `/update-skills` in Cursor.

See also: [references/skills-upstream-catalog.md](../references/skills-upstream-catalog.md), [references/skills-licenses.md](../references/skills-licenses.md).

## Always-on rules

| Rule | Source | Purpose |
|------|--------|---------|
| `agent-skills.mdc` | Template | Skill router and precedence |
| `ponytail.mdc` | [Ponytail](https://github.com/DietrichGebert/ponytail) | YAGNI / minimal code |
| `karpathy-guidelines.mdc` | [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Think first, surgical diffs |
| `i-have-adhd.mdc` | [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Action-first output formatting |
| `graphify.mdc` | Template | Knowledge-graph queries |

**Precedence:** template non-negotiables → ponytail → karpathy → i-have-adhd → domain skills.

## Lifecycle (addyosmani — primary)

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

Use addyosmani lifecycle by default. Superpowers skills below complement autonomous / subagent workflows.

## Superpowers ([obra/superpowers](https://github.com/obra/superpowers))

| Skill | Use when |
|-------|----------|
| `brainstorming` | `/brainstorm` — design before code |
| `writing-plans` | Detailed implementation plans |
| `executing-plans` | Batch plan execution |
| `subagent-driven-development` | Parallel subagent tasks |
| `superpowers-test-driven-development` | Red/green TDD (superpowers variant) |
| `systematic-debugging` | Root-cause debugging |
| `verification-before-completion` | Prove work before claiming done |
| `using-superpowers` | Meta: how superpowers skills chain |
| `using-git-worktrees` | Isolated worktrees |
| `dispatching-parallel-agents` | Parallel agent dispatch |
| `requesting-code-review` / `receiving-code-review` | Review workflows |
| `finishing-a-development-branch` | Branch completion |
| `writing-skills` | Author new skills |

## Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills))

| Command / skill | Purpose |
|-----------------|---------|
| `/grill-with-docs` → `grill-with-docs` | Alignment interview + CONTEXT.md / ADRs |
| `diagnosing-bugs` | Disciplined debug loop |
| `mp-tdd` | Red-green-refactor TDD |
| `improve-codebase-architecture` | Architecture deepening survey |
| `to-spec`, `implement`, `to-tickets`, `triage`, `ask-matt` | Spec and delivery helpers |
| `mp-code-review`, `domain-modeling` | Review and domain language |
| `setup-matt-pocock-skills` | One-time project setup |

## Design and UI

| Skill | Source |
|-------|--------|
| `taste-skill` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) |
| `ui-ux-pro-max` | [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) |
| `frontend-ui-engineering` | addyosmani |

## Anthropic OSS skills ([anthropics/skills](https://github.com/anthropics/skills))

Curated subset: `skill-creator`, `mcp-builder`, `webapp-testing`, `doc-coauthoring`, `theme-factory`, `brand-guidelines`, `canvas-design`, `internal-comms`, `web-artifacts-builder`, `algorithmic-art`.

**Not vendored:** `docx`, `pdf`, `pptx`, `xlsx` (source-available only).

## Community ([awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills))

`artifacts-builder`, `changelog-generator`, `connect-apps` (curated subset).

## Communication modes

| Mode | How |
|------|-----|
| Default | Karpathy + i-have-adhd (always-on rules) |
| `/caveman` | Opt-in ultra-compressed replies ([caveman](https://github.com/JuliusBrussee/caveman)) |
| Ponytail | Always-on minimal code; `/ponytail*` for intensity and audits |

## Ponytail

| Command | Skill | Purpose |
|---------|-------|---------|
| `/ponytail` | `ponytail` | Set intensity (`lite` / `full` / `ultra` / `off`) |
| `/ponytail-review` | `ponytail-review` | Over-engineering review of diff |
| `/ponytail-audit` | `ponytail-audit` | Repo-wide over-engineering audit |
| `/ponytail-debt` | `ponytail-debt` | Track deferred simplifications |
| `/ponytail-gain` | `ponytail-gain` | Benchmark impact summary |
| `/ponytail-help` | `ponytail-help` | Command reference |

## Local / template skills (preserved on sync)

- **`rtk-token-optimization`** — RTK shell compression; hook in `.cursor/hooks.json`
- **`awesome-agentic-patterns`** — live-fetch [agentic-patterns.com/llms.txt](https://agentic-patterns.com/llms.txt)
- **`graphify`** — repo knowledge graph (`make graph`, `graphify query`)

## Maintenance

| Command | Action |
|---------|--------|
| `/update-skills` | Run `./scripts/update-skills.sh` |
| Edit allowlist | `scripts/skills-manifest.json` then update |

Template maintainers run `./scripts/sync-skills.sh` from the cookiecutter repo root.

## Personas

Optional paste-in personas under `.cursor/agents/` (not auto-loaded).
