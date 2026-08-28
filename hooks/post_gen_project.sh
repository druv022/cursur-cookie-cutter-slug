#!/bin/bash
# Post-generation hook for cookiecutter template
# This script runs after the project is generated

set -e

# CookieCutter already changes into the project directory before running this hook
# So we're already in the project directory - no need to cd
PROJECT_DIR="{{ cookiecutter.project_slug }}"

echo "Running post-generation setup..."

# Make scripts executable
if [ -f "hooks/pre_gen_project.sh" ]; then
    chmod +x hooks/pre_gen_project.sh
fi
if [ -f "hooks/post_gen_project.sh" ]; then
    chmod +x hooks/post_gen_project.sh
fi

# Poetry and uv keep dependencies in pyproject.toml instead of requirements files
if [ "{{ cookiecutter.dependency_manager }}" = "poetry" ] || [ "{{ cookiecutter.dependency_manager }}" = "uv" ]; then
    rm -f requirements.txt requirements-dev.txt
    echo "{{ cookiecutter.dependency_manager }} setup: removed requirements.txt and requirements-dev.txt (deps in pyproject.toml)."
fi

# Keep only the selected CI/CD config; remove others
case "{{ cookiecutter.ci_cd }}" in
    github-actions)
        rm -f .gitlab-ci.yml
        rm -rf .circleci
        ;;
    gitlab-ci)
        rm -rf .github
        rm -rf .circleci
        ;;
    circleci)
        rm -rf .github
        rm -f .gitlab-ci.yml
        ;;
    none)
        rm -rf .github
        rm -f .gitlab-ci.yml
        rm -rf .circleci
        echo "CI/CD: none selected, removed all CI config."
        ;;
esac

# Remove Docker files if not requested
if [ "{{ cookiecutter.use_docker }}" != "y" ]; then
    rm -f Dockerfile docker-compose.yml
    echo "Docker: disabled, removed Dockerfile and docker-compose.yml."
fi

# Remove Makefile if not requested
if [ "{{ cookiecutter.use_makefile }}" != "y" ]; then
    rm -f Makefile
    echo "Makefile: disabled, removed Makefile."
fi

# Remove documentation tool files not selected
case "{{ cookiecutter.documentation_tool }}" in
    mkdocs)
        rm -f docs/conf.py docs/index.rst 2>/dev/null || true
        ;;
    sphinx)
        rm -f mkdocs.yml docs/index.md 2>/dev/null || true
        ;;
    none)
        rm -f mkdocs.yml docs/conf.py docs/index.rst docs/index.md 2>/dev/null || true
        ;;
esac

# Initialize git repository
if command -v git &> /dev/null; then
    if [ ! -d ".git" ]; then
        echo "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit from cookiecutter template"
        echo "Git repository initialized."
    else
        echo "Git repository already exists, skipping initialization."
    fi
else
    echo "WARNING: git is not installed. Skipping git initialization."
fi

# Create .env file from .env.example if it doesn't exist
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env with your configuration."
fi

# Cursor / RTK helpers (fail-open; never download binaries here)
if [ -f ".cursor/hooks/rtk-rewrite.sh" ]; then
    chmod +x .cursor/hooks/rtk-rewrite.sh
fi
if [ -f "scripts/install-rtk.sh" ]; then
    chmod +x scripts/install-rtk.sh
fi

if [ -f "scripts/update-skills.sh" ]; then
    chmod +x scripts/update-skills.sh
fi
if [ -f "scripts/sync_skills.py" ]; then
    chmod +x scripts/sync_skills.py
fi

echo ""
echo "Cursor agent tooling:"
if [ -f "SKILLS_LOCK.json" ]; then
    echo "  - Multi-upstream agent skills vendored (see SKILLS_LOCK.json)"
elif [ -f "AGENT_SKILLS_VERSION" ]; then
    echo "  - Agent skills vendored (see AGENT_SKILLS_VERSION)"
fi
echo "  - Lifecycle commands: /spec /plan /build /test /review /code-simplify /ship /webperf"
echo "  - Also: /brainstorm /grill-with-docs /caveman /update-skills"
if [ -f ".cursor/rules/karpathy-guidelines.mdc" ]; then
    echo "  - Karpathy + i-have-adhd output rules: always-on"
fi
if [ -f "PONYTAIL_VERSION" ] || [ -f "SKILLS_LOCK.json" ]; then
    echo "  - Ponytail YAGNI mode: always-on (.cursor/rules/ponytail.mdc); /ponytail* commands"
fi
echo "  - Agentic patterns: live fetch via .cursor/skills/awesome-agentic-patterns (agentic-patterns.com/llms.txt)"
if command -v rtk >/dev/null 2>&1 && rtk gain >/dev/null 2>&1; then
    echo "  - RTK: active on PATH ($(rtk --version 2>/dev/null || echo rtk)); project hook .cursor/hooks.json is ready"
else
    echo "  - RTK: not installed (or wrong package). Optional: ./scripts/install-rtk.sh then restart Cursor"
    echo "    Pin: see RTK_VERSION. Telemetry stays opt-in."
fi

# Display next steps
echo ""
echo "=========================================="
echo "Project {{ cookiecutter.project_name }} created successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_DIR"
if [ "{{ cookiecutter.dependency_manager }}" = "poetry" ]; then
    echo "2. Install dependencies: poetry install"
    echo "3. Activate virtual environment: poetry shell"
    echo "4. (Optional) Install pre-commit hooks: pre-commit install"
    echo "5. Update .env file with your configuration"
    {% if cookiecutter.testing_framework == 'pytest' %}echo "6. Run tests: poetry run pytest"{% else %}echo "6. Run tests: poetry run python -m unittest discover -v -s tests"{% endif %}
    echo "7. Read docs/DEVELOPMENT.md for Cursor workflow and day-1 setup"
elif [ "{{ cookiecutter.dependency_manager }}" = "uv" ]; then
    echo "2. Install dependencies: uv sync"
    echo "3. (Optional) Install pre-commit hooks: uv run pre-commit install"
    echo "4. Update .env file with your configuration"
    {% if cookiecutter.testing_framework == 'pytest' %}echo "5. Run tests: uv run pytest"{% else %}echo "5. Run tests: uv run python -m unittest discover -v -s tests"{% endif %}
    echo "6. Read docs/DEVELOPMENT.md for Cursor workflow and day-1 setup"
else
    echo "2. Create a virtual environment: python -m venv .venv"
    echo "3. Activate virtual environment: source .venv/bin/activate"
    echo "4. Install dependencies: pip install -r requirements-dev.txt"
    if [ "{{ cookiecutter.use_pre_commit }}" = "y" ]; then
        echo "5. Install pre-commit hooks: pre-commit install"
    fi
    echo "6. Update .env file with your configuration"
    {% if cookiecutter.testing_framework == 'pytest' %}echo "7. Run tests: pytest"{% else %}echo "7. Run tests: python -m unittest discover -v -s tests"{% endif %}
    echo "8. Read docs/DEVELOPMENT.md for Cursor workflow and day-1 setup"
fi
echo ""
echo "Happy coding!"
echo ""

