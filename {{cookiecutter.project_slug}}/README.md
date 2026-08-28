# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- Modern Python project structure
- Type hints and static type checking with MyPy
- Code formatting with Black and Ruff
- Comprehensive testing with {% if cookiecutter.testing_framework == 'pytest' %}pytest{% else %}unittest{% endif %}
- Pre-commit hooks for code quality
{% if cookiecutter.use_docker == 'y' %}
- Docker support for containerized development
{% endif %}
{% if cookiecutter.ci_cd != 'none' %}
- CI/CD pipelines ({% if cookiecutter.ci_cd == 'github-actions' %}GitHub Actions{% elif cookiecutter.ci_cd == 'gitlab-ci' %}GitLab CI{% elif cookiecutter.ci_cd == 'circleci' %}CircleCI{% endif %})
{% endif %}
- Cursor IDE optimized: multi-upstream agent skills, lifecycle slash commands, Ponytail YAGNI, Karpathy + i-have-adhd output rules, and optional RTK compression

## Cursor / AI tooling

This project ships Cursor Agent configuration under `.cursor/`:

| Layer | Path | Purpose |
|-------|------|---------|
| Rules | `.cursor/rules/*.mdc` | Router, ponytail, karpathy, i-have-adhd, graphify |
| Skills | `.cursor/skills/` | addyosmani lifecycle + superpowers, mattpocock, anthropic, UI/taste, local RTK/graphify/agentic |
| Commands | `.cursor/commands/` | `/spec` … `/ship`, `/brainstorm`, `/grill-with-docs`, `/caveman`, `/update-skills`, `/ponytail*` |
| References | `references/` | Shared checklists (definition of done, testing, security, …) |
| RTK hook | `.cursor/hooks.json` | Fail-open Shell rewrite through RTK when installed |
| graphify | `.cursor/rules/graphify.mdc` | Queryable codebase knowledge graph under `graphify-out/` |

Greenfield flow: `/spec` → `/plan` → `/build` → `/review` → `/ship`. Optional: `/brainstorm`, `/grill-with-docs`, `/ponytail-review`.

**Skills lock:** see `SKILLS_LOCK.json`. Refresh vendored skills with `./scripts/update-skills.sh`, `make update-skills`, or `/update-skills`.

**Communication stack:** always-on [Karpathy guidelines](https://github.com/multica-ai/andrej-karpathy-skills) + [i-have-adhd](https://github.com/ayghri/i-have-adhd) output rules. Opt-in token compression: `/caveman`.

**Ponytail:** always-on YAGNI mode from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail). See `SKILLS_LOCK.json` (legacy `PONYTAIL_VERSION`). Use `/ponytail lite|full|ultra|off`; `/ponytail-review` and `/ponytail-audit` for deletion-focused reviews.

**Knowledge graph (graphify):** build a navigable map of code and docs with `make graph-install && make graph`, then query with `make graph-query QUERY="…"` or ask the agent **use graphify**. After code edits, `make graph-update` refreshes the AST layer cheaply. Outputs live in `graphify-out/` (gitignored). See `.cursor/skills/graphify/SKILL.md`.

**Development guide:** after generation, follow [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for setup, Cursor workflow, daily commands, and troubleshooting.

**Agentic apps:** load `.cursor/skills/awesome-agentic-patterns` and **fetch** latest from [https://agentic-patterns.com/llms.txt](https://agentic-patterns.com/llms.txt) (do not use stale memory). Upstream catalogue: [nibzard/awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns).

**RTK (optional):** compresses verbose CLI output. Install with `./scripts/install-rtk.sh` (see `RTK_VERSION`), then restart Cursor. Bypass with `RTK_DISABLED=1`. Telemetry is opt-in only. Verify the correct binary with `rtk gain`.

Pinned skills versions: see `SKILLS_LOCK.json` (legacy: `AGENT_SKILLS_VERSION`, `PONYTAIL_VERSION`).

## Requirements

- Python 3.10+
- {% if cookiecutter.dependency_manager == 'poetry' %}Poetry{% elif cookiecutter.dependency_manager == 'uv' %}uv{% else %}pip or pip-tools{% endif %} for dependency management

## Installation

{% if cookiecutter.dependency_manager == 'poetry' %}
### Using Poetry (recommended for this project)

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies (creates virtual environment and installs dev dependencies)
poetry install

# Activate the virtual environment
poetry shell
```

### Alternative: using pip

You can export a lockfile and use pip: `poetry export -f requirements.txt --output requirements.txt` then `pip install -r requirements.txt`.
{% elif cookiecutter.dependency_manager == 'uv' %}
### Using uv

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install uv if it is not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create the virtual environment, lock dependencies, and install development tools
uv sync

# Run the application inside the managed environment
uv run python -m {{ cookiecutter.project_slug }}.main
```

Commit the generated `uv.lock` file to keep local, CI, and production installs reproducible.
{% else %}
### Using pip

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Alternative: using Poetry

You can use Poetry by running `poetry init` and adding dependencies from `pyproject.toml`, or install Poetry and run `poetry add $(cat requirements.txt)`.
{% endif %}

## Usage

```bash
# Run the application
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}python -m {{ cookiecutter.project_slug }}.main
{% if cookiecutter.use_makefile == 'y' %}

# Or using make
make run
{% endif %}
```

## Development

### Setup

1. Clone the repository
2. {% if cookiecutter.dependency_manager == 'poetry' %}Install dependencies: `poetry install` and activate: `poetry shell`{% elif cookiecutter.dependency_manager == 'uv' %}Install dependencies: `uv sync`{% else %}Create a virtual environment and install development dependencies: `pip install -r requirements-dev.txt`{% endif %}
3. Install pre-commit hooks: `{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pre-commit install`
4. Copy `.env.example` to `.env` and configure

### Running Tests

```bash
# Run all tests
{% if cookiecutter.testing_framework == 'pytest' %}
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pytest

# Run with coverage
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pytest --cov={{ cookiecutter.project_slug }} --cov-report=html

# Run specific test file
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pytest tests/test_main.py
{% else %}
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}python -m unittest discover -v -s tests -p "test_*.py"

# Run with coverage
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}coverage run -m unittest discover -s tests -p "test_*.py"
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}coverage report
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}coverage html
{% endif %}
{% if cookiecutter.use_makefile == 'y' %}

# Or using make
make test
{% endif %}
```

### Code Quality

```bash
# Format code
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}black .
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}ruff check --fix .

# Type checking
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}mypy src
{% if cookiecutter.use_makefile == 'y' %}

# Run all checks
make lint
make format
make type-check
{% endif %}

# Or use pre-commit
{% if cookiecutter.dependency_manager == 'poetry' %}poetry run {% elif cookiecutter.dependency_manager == 'uv' %}uv run {% endif %}pre-commit run --all-files
```

{% if cookiecutter.use_docker == 'y' %}
### Docker

```bash
# Build image
docker build -t {{ cookiecutter.project_slug }}:latest .

# Run container
docker-compose up
{% if cookiecutter.use_makefile == 'y' %}

# Or using make
make docker-build
make docker-up
{% endif %}
```
{% endif %}

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   └── {{ cookiecutter.project_slug }}/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   ├── DEVELOPMENT.md
│   ├── CONTRIBUTING.md
│   └── ARCHITECTURE.md
{% if cookiecutter.documentation_tool == 'mkdocs' %}
│   └── index.md
{% elif cookiecutter.documentation_tool == 'sphinx' %}
│   ├── conf.py
│   └── index.rst
{% endif %}
{% if cookiecutter.ci_cd == 'github-actions' %}
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
{% elif cookiecutter.ci_cd == 'gitlab-ci' %}
├── .gitlab-ci.yml
{% elif cookiecutter.ci_cd == 'circleci' %}
├── .circleci/
│   └── config.yml
{% endif %}
├── .pre-commit-config.yaml
├── pyproject.toml
{% if cookiecutter.dependency_manager not in ['poetry', 'uv'] %}
├── requirements.txt
├── requirements-dev.txt
{% endif %}
{% if cookiecutter.use_docker == 'y' %}
├── Dockerfile
├── docker-compose.yml
{% endif %}
{% if cookiecutter.use_makefile == 'y' %}
├── Makefile
{% endif %}
{% if cookiecutter.documentation_tool == 'mkdocs' %}
├── mkdocs.yml
{% endif %}
├── LICENSE
└── README.md
```

{% if cookiecutter.documentation_tool == 'mkdocs' %}
## Documentation

Build and serve the docs with MkDocs:

```bash
pip install mkdocs
mkdocs serve
```
{% elif cookiecutter.documentation_tool == 'sphinx' %}
## Documentation

Build the docs with Sphinx:

```bash
pip install sphinx
cd docs && sphinx-build -b html . _build
```
{% endif %}

## Configuration

Copy `.env.example` to `.env` and configure your environment variables:

```bash
cp .env.example .env
```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the {{ cookiecutter.license }} License - see the LICENSE file for details.

## Author

**{{ cookiecutter.author_name }}**

- Email: {{ cookiecutter.author_email }}
- GitHub: [@{{ cookiecutter.github_username }}](https://github.com/{{ cookiecutter.github_username }})

## Acknowledgments

- Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- Optimized for [Cursor IDE](https://cursor.sh/)

