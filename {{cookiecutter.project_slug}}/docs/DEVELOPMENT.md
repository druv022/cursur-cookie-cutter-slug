# How To Develop {{ cookiecutter.project_name }} After Generation

This guide covers day-0 and day-1 work after Cookiecutter creates the project: environment setup, Cursor workflow, daily quality commands, and known scaffold limits.

## Prerequisites

- Python 3.10+
- {% if cookiecutter.dependency_manager == 'poetry' %}Poetry{% elif cookiecutter.dependency_manager == 'uv' %}uv{% else %}pip (and a virtual environment){% endif %}
- [Cursor](https://cursor.sh/) IDE (for rules, skills, and slash commands)
{% if cookiecutter.use_docker == 'y' %}- Docker and Docker Compose (optional, if you use containers)
{% endif %}- Git

## First-time setup

1. Open the **generated project root** in Cursor — the folder that contains `pyproject.toml`, `src/`, and `.cursor/`. Do not keep working from the Cookiecutter template repository.
2. Install dependencies:
{% if cookiecutter.dependency_manager == 'poetry' %}
   ```bash
   poetry install
   poetry shell
   ```
{% elif cookiecutter.dependency_manager == 'uv' %}
   ```bash
   uv sync
   ```
   Commit the generated `uv.lock` so local, CI, and production installs stay reproducible.
{% else %}
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```
{% endif %}
{% if cookiecutter.use_pre_commit == 'y' %}
3. Install pre-commit hooks:
   ```bash
   {% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pre-commit install
   ```
{% else %}
3. Pre-commit was not selected at generation time. You can still add hooks later if you keep `.pre-commit-config.yaml`.
{% endif %}
4. Configure environment variables if your app needs them. Create a `.env` from a project template when one exists (some scaffolds reference `.env.example`; add that file yourself if it is missing).
5. Establish a baseline — run the app and the test suite once:
   ```bash
   {% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}python -m {{ cookiecutter.project_slug }}.main
   {% if cookiecutter.testing_framework == 'pytest' %}{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pytest
   {% else %}{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}python -m unittest discover -v -s tests -p "test_*.py"
   {% endif %}
   ```
{% if cookiecutter.use_makefile == 'y' %}
   Or: `make run` and `make test`.
{% endif %}

**Note:** The Cookiecutter post-generation hook may already have run `git init` and created an initial commit. Treat that as your starting history.

### Expected results

- Dependencies install without error.
- The sample entry point runs.
- The sample tests pass.
- In Cursor Agent chat, slash commands such as `/spec` and `/build` appear when you type `/`.

## How Cursor tooling works here

| Layer | Path | What it does |
|-------|------|----------------|
| Rules | `.cursor/rules/*.mdc` | Short policies; `agent-skills.mdc` routes work to skills; `ponytail.mdc` enforces YAGNI/minimal code |
| Skills | `.cursor/skills/` | Detailed playbooks (spec, TDD, review, security, ponytail, …) |
| Commands | `.cursor/commands/` | Slash entry points: `/spec` `/plan` `/build` `/test` `/review` `/code-simplify` `/ship` `/webperf` and `/ponytail*` |
| Agents | `.cursor/agents/` | Optional specialist personas (used by `/ship`; not auto-loaded) |
| References | `references/` | Checklists (definition of done, testing, security, performance) |
| Hooks | `.cursor/hooks.json` | Optional Shell rewrite through RTK when installed |
| graphify | `.cursor/rules/graphify.mdc` | Prefer `graphify query` for architecture questions when `graphify-out/graph.json` exists |

Plain chat does **not** dump every skill into context or run the lifecycle for you. Always-on rules apply; the agent should load matching skills when relevant. For the designed workflow, **invoke the slash commands** yourself.

See [CURSOR_AGENT_SKILLS.md](CURSOR_AGENT_SKILLS.md) for the command-to-skill map.

## Recommended workflow

For new features or greenfield work:

1. `/spec` — write acceptance criteria (`SPEC.md`).
2. `/plan` — break work into vertical tasks (`tasks/plan.md`, `tasks/todo.md`).
3. `/build` — implement one task with tests (or `/build auto` after a real spec exists).
4. `/review` — five-axis review of the change.
5. `/ponytail-review` — optional deletion-focused pass for over-engineering (complements `/review`).
6. `/ship` — launch readiness, specialist fan-out, and rollback plan.

Order is guidance, not a hard lock. Reordering is fine for small bugs (`/test` or `/build`), cleanup (`/code-simplify`), or a launch check on an existing branch (`/ship`). Skipping `/spec` before a non-trivial feature is costly: you get code without agreed acceptance criteria. `/build auto` stops if no spec is found at a known path (`SPEC.md`, `docs/SPEC.md`, or under `spec/`).

Before calling work done, use [references/definition-of-done.md](../references/definition-of-done.md).

## Daily development commands

{% if cookiecutter.dependency_manager == 'poetry' %}
```bash
poetry run black .
poetry run ruff check --fix .
poetry run mypy src
{% if cookiecutter.testing_framework == 'pytest' %}poetry run pytest
{% else %}poetry run python -m unittest discover -v -s tests -p "test_*.py"
{% endif %}
poetry run pre-commit run --all-files
```
{% elif cookiecutter.dependency_manager == 'uv' %}
```bash
uv run black .
uv run ruff check --fix .
uv run mypy src
{% if cookiecutter.testing_framework == 'pytest' %}uv run pytest
{% else %}uv run python -m unittest discover -v -s tests -p "test_*.py"
{% endif %}
uv run pre-commit run --all-files
```
{% else %}
```bash
black .
ruff check --fix .
mypy src
{% if cookiecutter.testing_framework == 'pytest' %}pytest
{% else %}python -m unittest discover -v -s tests -p "test_*.py"
{% endif %}
pre-commit run --all-files
```
{% endif %}
{% if cookiecutter.use_makefile == 'y' %}

Makefile shortcuts: `make format`, `make lint`, `make type-check`, `make test`, `make run`.
{% endif %}
{% if cookiecutter.use_docker == 'y' %}

### Docker

```bash
docker build -t {{ cookiecutter.project_slug }}:latest .
docker-compose up
```
{% if cookiecutter.use_makefile == 'y' %}
Or: `make docker-build` and `make docker-up`.
{% endif %}
Validate that the image installs and runs the `src/` package before relying on it in production.
{% endif %}
{% if cookiecutter.ci_cd != 'none' %}

### CI

This project includes {% if cookiecutter.ci_cd == 'github-actions' %}GitHub Actions (`.github/workflows/`){% elif cookiecutter.ci_cd == 'gitlab-ci' %}GitLab CI (`.gitlab-ci.yml`){% elif cookiecutter.ci_cd == 'circleci' %}CircleCI (`.circleci/config.yml`){% endif %}. Push a branch and confirm lint, tests, and security jobs match what you run locally. Prefer locked/reproducible installs in CI when your manager supports them.
{% endif %}

## Optional: RTK

RTK compresses verbose CLI output so agent sessions keep more useful context.

1. Run `./scripts/install-rtk.sh` (see `RTK_VERSION`).
2. Restart Cursor.
3. Confirm with `rtk gain`.
4. Bypass anytime with `RTK_DISABLED=1`.

The project hook is fail-open: if RTK is missing, Shell commands still run.

## Optional: graphify (knowledge graph)

[graphify](https://pypi.org/project/graphifyy/) turns this repo into a queryable knowledge graph — useful for architecture questions, cross-file relationships, and onboarding.

1. Run `./scripts/install-graphify.sh` (or `make graph-install`).
2. Build the graph: `make graph` (writes `graphify-out/graph.html` and `GRAPH_REPORT.md`).
3. Query: `make graph-query QUERY="How does the entry point work?"` or ask the agent **use graphify**.
4. After editing code: `make graph-update` (AST-only, no API cost).

The always-on rule `.cursor/rules/graphify.mdc` tells agents to prefer `graphify query` over reading the whole tree when `graphify-out/graph.json` exists. See `.cursor/skills/graphify/SKILL.md`.

Optional: set `GEMINI_API_KEY` before `make graph` for richer semantic extraction on markdown docs.

## Ponytail (always on)

[Ponytail](https://github.com/DietrichGebert/ponytail) ships as an always-on Cursor rule (`.cursor/rules/ponytail.mdc`) that pushes the agent toward minimal, necessary code: reuse existing helpers, prefer stdlib and native features, avoid speculative abstractions.

- **Intensity:** `/ponytail lite|full|ultra|off` (default is full via the always-on rule)
- **Review for bloat:** `/ponytail-review` on your diff, or `/ponytail-audit` for the whole repo
- **Upstream pin:** `PONYTAIL_VERSION`

Ponytail complements the lifecycle commands; it does not replace `/spec`, `/build`, or `/review`. This template's unit-test coverage rule still applies — ponytail minimizes implementation size, not test obligations.

## What the scaffold does not give you

Treat the generated tree as a starting point, not a finished product:

- Choosing Django, Flask, FastAPI, or Pydantic mainly adds **dependencies**. It does not generate a full working framework application.
- Some Cursor rules assume pytest, uv, or FastAPI. If you chose other options, align rules under `.cursor/rules/` with your stack.
- Coverage “100%” guidance in rules may not be enforced by `fail_under` in tooling — set that bar explicitly if you need a gate.
- Docs such as [ARCHITECTURE.md](ARCHITECTURE.md) may describe goals (for example multi-stage Docker or health checks) that you still need to implement or verify.
- If README mentions `.env.example` and the file is absent, add it for your team.

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| Slash commands missing | Confirm Cursor opened the generated project root (folder with `.cursor/commands/`). Restart Cursor after generation. |
| Agent ignores skills | Invoke `/spec`, `/plan`, `/build`, etc., or ask it to follow the matching skill under `.cursor/skills/`. |
| Import errors for the package | Install the project in editable mode via your dependency manager; keep the `src/` layout; run via `{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}python -m {{ cookiecutter.project_slug }}.main`. |
| Pre-commit fails on commit | Run `{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pre-commit run --all-files`, fix reported issues, commit again. |
| `/build auto` stops immediately | Create a real spec first (`/spec` → `SPEC.md`). A README alone does not count. |
| graphify query fails | Run `make graph-install && make graph` first. Confirm `graphify-out/graph.json` exists. |
| Wrong repo / wrong tooling | You may still have the Cookiecutter template open. Close it and open the generated project folder. |
| Docker run fails | Confirm the image installs the package and that `PYTHONPATH` / entrypoint match `src/`. |

## Related docs

- [README.md](../README.md) — install and run
- [CONTRIBUTING.md](CONTRIBUTING.md) — PRs, style, commits
- [ARCHITECTURE.md](ARCHITECTURE.md) — structure and design notes
- [CURSOR_AGENT_SKILLS.md](CURSOR_AGENT_SKILLS.md) — skills and slash commands
- [references/definition-of-done.md](../references/definition-of-done.md) — standing quality bar
- [references/testing-patterns.md](../references/testing-patterns.md) — testing guidance
- [references/security-checklist.md](../references/security-checklist.md) — security checklist
