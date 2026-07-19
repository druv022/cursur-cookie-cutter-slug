# Cookiecutter Cursor Template

A cookiecutter template for creating Python projects optimized for Cursor IDE with best practices for scalable implementation.

## Features

- **Python-focused**: Modern Python project structure with type hints
- **Cursor IDE optimized**: Includes `.cursorrules` for AI-assisted development
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
cookiecutter /path/to/this/template
```

Or use it directly from a directory:

```bash
cookiecutter .
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
{{cookiecutter.project_slug}}/
├── cookiecutter.json          # Template configuration
├── hooks/                     # Pre/post-generation hooks
│   ├── pre_gen_project.sh
│   └── post_gen_project.sh
└── {{cookiecutter.project_slug}}/  # Template files
    ├── .cursorrules           # Cursor IDE AI guidelines
    ├── .cursor/               # Cursor settings
    ├── .vscode/               # VS Code/Cursor workspace settings
    ├── .github/                # GitHub workflows
    ├── src/                    # Source code
    ├── tests/                  # Test suite
    ├── docs/                   # Documentation
    ├── pyproject.toml          # Python project config
    ├── requirements.txt        # Production dependencies (pip/pip-tools)
    ├── requirements-dev.txt   # Development dependencies (pip/pip-tools)
    ├── Dockerfile             # Container configuration
    ├── docker-compose.yml     # Docker Compose setup
    ├── Makefile               # Development commands
    └── README.md              # Project README template
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

- `.cursor/.cursorrules`: Comprehensive AI coding guidelines
- `.cursor/settings.json`: Cursor-specific configuration
- `.vscode/`: Workspace settings optimized for Python development

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

## Usage Example

```bash
# Generate a new project
cookiecutter .

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
- Follows Python best practices and modern tooling standards

