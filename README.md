# Cookiecutter Cursor Template

A cookiecutter template for creating Python projects optimized for Cursor IDE with best practices for scalable implementation.

## Features

- **Python-focused**: Modern Python project structure with type hints
- **Cursor IDE optimized**: Includes `.cursorrules` for AI-assisted development
- **Best practices**: Pre-configured with modern tooling (Black, Ruff, MyPy, Pytest)
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
- Dependency manager
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
    ├── requirements.txt        # Production dependencies
    ├── requirements-dev.txt   # Development dependencies
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

## Usage Example

```bash
# Generate a new project
cookiecutter .

# Follow the prompts:
# project_name [My Awesome Project]: My Project
# project_description [A scalable Python project...]: My description
# python_framework [none]: fastapi
# ...

# Navigate to the generated project
cd my_project

# Set up the environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install

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

