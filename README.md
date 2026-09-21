# Cookiecutter Cursor Template

A cookiecutter template for creating Python projects optimized for Cursor IDE with best practices for scalable implementation.

## Features

- **Python-focused**: Modern Python project structure with type hints
- **Cursor IDE optimized**: Multi-upstream agent skills (addyosmani, superpowers, mattpocock, anthropic, taste, UI/UX, karpathy, i-have-adhd, caveman) + RTK + graphify + ponytail; `/update-skills` refresh command
- **Best practices**: Pre-configured with modern tooling (Black, Ruff, MyPy, Pytest)
- **Flexible environments**: Choose Poetry, uv, pip, or pip-tools for dependency management
- **CI/CD ready**: GitHub Actions workflows included
- **Docker support**: Development and production containers
- **Pre-commit hooks**: Automated code quality checks
- **Comprehensive documentation**: README, CONTRIBUTING, and ARCHITECTURE docs

## Quick Start

### Prerequisites

- Python 3.10+
- cookiecutter: `pip install cookiecutter`

### Generate a New Project

```bash
./generate.sh
```

Or from another directory:

```bash
/path/to/this/template/generate.sh -o ~/projects
```

`generate.sh` passes `--overwrite-if-exists` so re-running against an existing project **updates template files** instead of failing with `directory already exists`. When a replay file exists for the same `project_slug`, it also passes `--replay` to reuse your last answers.

Raw cookiecutter still works; add `-f` manually to update an existing project:

```bash
cookiecutter /path/to/this/template -f --replay
```

You'll be prompted for:
- Project name
- Description
- Author information
- License
- Python framework (Django, Flask, FastAPI, etc.)
- Dependency manager (Poetry, uv, pip, or pip-tools)
- CI/CD preference
- Testing framework
- Documentation tool
- Docker and pre-commit preferences

## Template Structure

```
.
├── cookiecutter.json
├── hooks/
│   ├── pre_gen_project.sh
│   └── post_gen_project.sh
├── scripts/
│   ├── skills-manifest.json   # Upstream allowlist and pins
│   ├── sync_skills.py         # Core sync engine
│   ├── sync-skills.sh         # Re-vendor all skills into template
│   ├── sync-agent-skills.sh   # Wrapper: addyosmani only
│   └── sync-ponytail.sh       # Wrapper: ponytail only
└── {{cookiecutter.project_slug}}/
    ├── .cursor/
    │   ├── rules/             # Router, ponytail, karpathy, i-have-adhd, graphify
    │   ├── skills/            # ~78 vendored + local RTK/agentic/graphify
    │   ├── commands/          # Lifecycle, brainstorm, grill, caveman, update-skills, ponytail*
    │   ├── agents/
    │   ├── hooks.json
    │   └── hooks/
    ├── references/            # Checklists + skills catalog/licenses
    ├── SKILLS_LOCK.json       # Unified upstream pin lockfile
    ├── scripts/
    │   ├── skills-manifest.json
    │   ├── sync_skills.py
    │   └── update-skills.sh   # Generated-project refresh
    ├── RTK_VERSION
    ├── scripts/install-rtk.sh
    ├── scripts/install-graphify.sh
    ├── .vscode/
    ├── src/
    ├── tests/
    └── README.md
```

## What's Included

### Development Tools

- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Pytest**: Testing framework with coverage
- **Pre-commit**: Git hooks for quality checks
- **Bandit**: Security linting

### CI/CD

- GitHub Actions workflows for:
  - Linting and formatting checks
  - Testing across multiple Python versions
  - Security scanning
  - Package building
  - Automated releases

### Cursor IDE Integration

- **Rules** (`.cursor/rules/*.mdc`): Router, ponytail (YAGNI), karpathy (think first), i-have-adhd (action-first output), graphify.
- **Skills** (`.cursor/skills/`): Curated bundle from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), [superpowers](https://github.com/obra/superpowers), [mattpocock/skills](https://github.com/mattpocock/skills), [anthropics/skills](https://github.com/anthropics/skills), [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills), [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [taste-skill](https://github.com/leonxlnx/taste-skill), [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), [i-have-adhd](https://github.com/ayghri/i-have-adhd), [caveman](https://github.com/JuliusBrussee/caveman), plus local RTK/agentic-patterns/graphify and [ponytail](https://github.com/DietrichGebert/ponytail).
- **Commands**: lifecycle (`/spec` … `/ship`), `/brainstorm`, `/grill-with-docs`, `/caveman`, `/update-skills`, `/ponytail*`
- **Lock file**: `SKILLS_LOCK.json` records pinned SHAs for every upstream source.

#### Re-sync all skills (template maintainers)

```bash
./scripts/sync-skills.sh                    # all sources per skills-manifest.json
./scripts/sync-skills.sh --source superpowers
```

#### Re-sync single sources (legacy wrappers)

```bash
./scripts/sync-agent-skills.sh   # addyosmani only
./scripts/sync-ponytail.sh       # ponytail only
```

Generated projects refresh with `./scripts/update-skills.sh` or `/update-skills`.

Local skills (`rtk-token-optimization`, `awesome-agentic-patterns`, `graphify`) are preserved across sync.

`cookiecutter.json` sets `_copy_without_render` for `.cursor/skills`, `.cursor/agents`, and `references` so vendored Markdown with `{{ }}` examples is copied verbatim.

### Documentation

- README template with setup instructions
- CONTRIBUTING guidelines
- ARCHITECTURE documentation

## Customization

You can customize the template by:

1. Modifying `cookiecutter.json` to add/remove prompts
2. Editing template files in `{{cookiecutter.project_slug}}/`
3. Adding conditional logic based on user choices
4. Extending hooks for additional setup steps

## Template Development

### Run the Template Tests

```bash
python -m pip install -r requirements-dev.txt
pytest tests/ -v
```

The tests generate projects for every dependency-manager option and verify the uv configuration across supported CI providers.

### Working with GitHub Actions Syntax

When including GitHub Actions workflow files (`.yml` files in `.github/workflows/`), you need to escape GitHub Actions expressions to prevent cookiecutter from interpreting them as template variables.

**Problem**: GitHub Actions uses `${{ }}` syntax for expressions (e.g., `${{ secrets.GITHUB_TOKEN }}`), which conflicts with cookiecutter's Jinja2 templating.

**Solution**: Use Jinja2's `{% raw %}` blocks to escape GitHub Actions syntax:

```yaml
# In template file (.github/workflows/release.yml)
env:
  GITHUB_TOKEN: ${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}
  TWINE_PASSWORD: ${% raw %}{{ secrets.PYPI_API_TOKEN }}{% endraw %}
```

This will render correctly in the generated project as:
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### Hooks

The template includes two hooks:

- **`pre_gen_project.sh`**: Runs before project generation. Use for validation and checks.
- **`post_gen_project.sh`**: Runs after project generation. Use for setup tasks like git initialization.

**Important**: The `post_gen_project.sh` hook runs from within the generated project directory. Do not include a `cd` command to change into the project directory, as cookiecutter already does this automatically.

Example hook structure:
```bash
#!/bin/bash
set -e

# CookieCutter already changes into the project directory before running this hook
# So we're already in the project directory - no need to cd
PROJECT_DIR="{{ cookiecutter.project_slug }}"

# Your setup commands here
echo "Setting up project..."
```

### Template Variables

Use `{{ cookiecutter.variable_name }}` syntax in template files. Variables are defined in `cookiecutter.json` and can include:

- Simple strings
- Lists (for choices)
- Jinja2 expressions (e.g., `{{ cookiecutter.project_name.lower().replace(' ', '_') }}`)

### Troubleshooting

**Issue**: Template generation fails with "undefined variable" error
- **Solution**: Ensure all variables used in templates are defined in `cookiecutter.json`

**Issue**: GitHub Actions workflows have incorrect syntax after generation
- **Solution**: Use `{% raw %}` blocks around `${{ }}` expressions in workflow files

**Issue**: Post-generation hook fails with "directory not found"
- **Solution**: Remove any `cd` commands from `post_gen_project.sh` - cookiecutter already runs hooks from the project directory

**Issue**: `Error: "my_project" directory already exists`
- **Solution**: Use `./generate.sh` (auto update mode) or `cookiecutter . -f --replay` to refresh template files in the existing project. Review `git diff` before committing. Generated projects can also run `./scripts/update-from-template.sh` with `COOKIECUTTER_TEMPLATE` set.

## Usage Example

```bash
# Generate a new project (or update an existing one with the same slug)
./generate.sh

# Follow the prompts:
# project_name [My Awesome Project]: My Project
# project_description [A scalable Python project...]: My description
# python_framework [none]: fastapi
# dependency_manager [poetry]: uv
# ...

# Navigate to the generated project
cd my_project

# Set up the uv-managed environment
uv sync
uv run pre-commit install

# Read docs/DEVELOPMENT.md for Cursor workflow, daily commands, and troubleshooting

# Start developing!
```

## License

This template is provided as-is. Generated projects will use the license you select during project generation.

## Contributing

Contributions to improve this template are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

- Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- Optimized for [Cursor IDE](https://cursor.sh/)

Open-source upstreams vendored or used by this template:

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- [obra/superpowers](https://github.com/obra/superpowers)
- [anthropics/skills](https://github.com/anthropics/skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill)
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- [rtk-ai/rtk](https://github.com/rtk-ai/rtk)
- [nibzard/awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns)

Not all of these are MIT. See [`{{cookiecutter.project_slug}}/references/skills-licenses.md`]({{cookiecutter.project_slug}}/references/skills-licenses.md) for per-source license details.

