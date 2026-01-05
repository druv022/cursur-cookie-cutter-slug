#!/bin/bash
# Pre-generation hook for cookiecutter template
# This script runs before the project is generated

set -e

echo "Running pre-generation checks..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed."
    exit 1
fi

# Check Python version (3.10+)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "ERROR: Python 3.10 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python version check passed: $PYTHON_VERSION"

# Validate project slug
PROJECT_SLUG="{{ cookiecutter.project_slug }}"
if [[ ! "$PROJECT_SLUG" =~ ^[a-z][a-z0-9_]*$ ]]; then
    echo "ERROR: Project slug must be lowercase, start with a letter, and contain only letters, numbers, and underscores."
    echo "Got: $PROJECT_SLUG"
    exit 1
fi

echo "Project slug validation passed: $PROJECT_SLUG"

# Check if cookiecutter is installed (optional, just a warning)
if ! command -v cookiecutter &> /dev/null; then
    echo "WARNING: cookiecutter is not installed. Install with: pip install cookiecutter"
fi

echo "Pre-generation checks completed successfully!"

