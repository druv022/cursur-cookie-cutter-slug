.PHONY: help install install-dev test lint format type-check clean run docker-build docker-up docker-down

# Variables
PYTHON := python3
PIP := pip
VENV := .venv
PYTHON_VENV := $(VENV)/bin/python
PIP_VENV := $(VENV)/bin/pip

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	@echo "Installing production dependencies..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry install --no-dev
{% else %}
	$(PIP) install -r requirements.txt
{% endif %}

install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry install
	@if [ "{{ cookiecutter.use_pre_commit }}" = "y" ]; then \
		poetry run pre-commit install; \
	fi
{% else %}
	$(PIP) install -r requirements-dev.txt
	@if [ "{{ cookiecutter.use_pre_commit }}" = "y" ]; then \
		pre-commit install; \
	fi
{% endif %}

venv: ## Create virtual environment
	@echo "Creating virtual environment..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	@echo "Using Poetry: run 'poetry shell' to activate."
{% else %}
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created. Activate with: source $(VENV)/bin/activate"
{% endif %}

test: ## Run tests
	@echo "Running tests..."
{% if cookiecutter.testing_framework == 'pytest' %}
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run pytest tests/ -v --cov={{ cookiecutter.project_slug }} --cov-report=term-missing --cov-report=html
{% else %}
	pytest tests/ -v --cov={{ cookiecutter.project_slug }} --cov-report=term-missing --cov-report=html
{% endif %}
{% else %}
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run coverage run -m unittest discover -v -s tests -p "test_*.py"
	poetry run coverage report
	poetry run coverage html
{% else %}
	coverage run -m unittest discover -v -s tests -p "test_*.py"
	coverage report
	coverage html
{% endif %}
{% endif %}

test-watch: ## Run tests in watch mode (pytest only; unittest runs once)
	@echo "Running tests in watch mode..."
{% if cookiecutter.testing_framework == 'pytest' %}
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run pytest-watch tests/
{% else %}
	pytest-watch tests/
{% endif %}
{% else %}
	@echo "Unittest: run 'make test' (watch not configured)."
	$(MAKE) test
{% endif %}

lint: ## Run linters
	@echo "Running linters..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run ruff check .
	poetry run mypy src
{% else %}
	ruff check .
	mypy src
{% endif %}

format: ## Format code
	@echo "Formatting code..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run black .
	poetry run ruff check --fix .
{% else %}
	black .
	ruff check --fix .
{% endif %}

type-check: ## Run type checker
	@echo "Running type checker..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run mypy src
{% else %}
	mypy src
{% endif %}

clean: ## Clean build artifacts
	@echo "Cleaning..."
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .mypy_cache .ruff_cache htmlcov .coverage dist build
{% if cookiecutter.testing_framework == 'pytest' %}
	rm -rf .pytest_cache
{% endif %}

run: ## Run the application
	@echo "Running application..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run python -m {{ cookiecutter.project_slug }}.main
{% else %}
	python -m {{ cookiecutter.project_slug }}.main
{% endif %}

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t {{ cookiecutter.project_slug }}:latest .

docker-up: ## Start Docker containers
	@echo "Starting Docker containers..."
	docker-compose up -d

docker-down: ## Stop Docker containers
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

pre-commit: ## Run pre-commit hooks on all files
	@echo "Running pre-commit hooks..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry run pre-commit run --all-files
{% else %}
	pre-commit run --all-files
{% endif %}

