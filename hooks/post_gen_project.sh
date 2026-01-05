#!/bin/bash
# Post-generation hook for cookiecutter template
# This script runs after the project is generated

set -e

PROJECT_DIR="{{ cookiecutter.project_slug }}"
cd "$PROJECT_DIR"

echo "Running post-generation setup..."

# Make scripts executable
if [ -f "hooks/pre_gen_project.sh" ]; then
    chmod +x hooks/pre_gen_project.sh
fi
if [ -f "hooks/post_gen_project.sh" ]; then
    chmod +x hooks/post_gen_project.sh
fi

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

# Display next steps
echo ""
echo "=========================================="
echo "Project {{ cookiecutter.project_name }} created successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_DIR"
echo "2. Create a virtual environment: python -m venv .venv"
echo "3. Activate virtual environment: source .venv/bin/activate"
echo "4. Install dependencies: pip install -r requirements-dev.txt"
if [ "{{ cookiecutter.use_pre_commit }}" = "y" ]; then
    echo "5. Install pre-commit hooks: pre-commit install"
fi
echo "6. Update .env file with your configuration"
echo "7. Run tests: pytest"
echo ""
echo "Happy coding!"
echo ""

