# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- Modern Python project structure
- Type hints and static type checking with MyPy
- Code formatting with Black and Ruff
- Comprehensive testing with pytest
- Pre-commit hooks for code quality
- Docker support for containerized development
- CI/CD pipelines with GitHub Actions
- Cursor IDE optimized with `.cursorrules`

## Requirements

- Python 3.10+
- pip or poetry for dependency management

## Installation

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

### Using poetry

```bash
# Install poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Usage

```bash
# Run the application
python -m {{ cookiecutter.project_slug }}.main

# Or using make
make run
```

## Development

### Setup

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Install pre-commit hooks: `pre-commit install`
5. Copy `.env.example` to `.env` and configure

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{ cookiecutter.project_slug }} --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Or using make
make test
```

### Code Quality

```bash
# Format code
black .
ruff check --fix .

# Type checking
mypy {{ cookiecutter.project_slug }}

# Run all checks
make lint
make format
make type-check

# Or use pre-commit
pre-commit run --all-files
```

### Docker

```bash
# Build image
docker build -t {{ cookiecutter.project_slug }}:latest .

# Run container
docker-compose up

# Or using make
make docker-build
make docker-up
```

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
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── ARCHITECTURE.md
├── scripts/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── .cursorrules
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

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

