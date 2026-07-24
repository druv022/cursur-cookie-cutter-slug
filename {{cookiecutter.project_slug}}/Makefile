.PHONY: help install install-dev test lint format type-check clean run docker-build docker-up docker-down graph-install graph graph-update graph-query

# Variables
PYTHON := python3
PIP := pip
VENV := .venv
PYTHON_VENV := $(VENV)/bin/python
PIP_VENV := $(VENV)/bin/pip
{% if cookiecutter.dependency_manager == 'poetry' %}
RUNNER := poetry run
{% elif cookiecutter.dependency_manager == 'uv' %}
RUNNER := uv run
{% else %}
RUNNER :=
{% endif %}

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	@echo "Installing production dependencies..."
{% if cookiecutter.dependency_manager == 'poetry' %}
	poetry install --no-dev
{% elif cookiecutter.dependency_manager == 'uv' %}
	uv sync --no-dev
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
{% elif cookiecutter.dependency_manager == 'uv' %}
	uv sync
	@if [ "{{ cookiecutter.use_pre_commit }}" = "y" ]; then \
		uv run pre-commit install; \
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
{% elif cookiecutter.dependency_manager == 'uv' %}
	uv sync
	@echo "uv created .venv. Run commands with 'uv run' or activate with: source $(VENV)/bin/activate"
{% else %}
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created. Activate with: source $(VENV)/bin/activate"
{% endif %}

test: ## Run tests
	@echo "Running tests..."
{% if cookiecutter.testing_framework == 'pytest' %}
	$(RUNNER) pytest tests/ -v --cov={{ cookiecutter.project_slug }} --cov-report=term-missing --cov-report=html
{% else %}
	$(RUNNER) coverage run -m unittest discover -v -s tests -p "test_*.py"
	$(RUNNER) coverage report
	$(RUNNER) coverage html
{% endif %}

test-watch: ## Run tests in watch mode (pytest only; unittest runs once)
	@echo "Running tests in watch mode..."
{% if cookiecutter.testing_framework == 'pytest' %}
	$(RUNNER) pytest-watch tests/
{% else %}
	@echo "Unittest: run 'make test' (watch not configured)."
	$(MAKE) test
{% endif %}

lint: ## Run linters
	@echo "Running linters..."
	$(RUNNER) ruff check .
	$(RUNNER) mypy src

format: ## Format code
	@echo "Formatting code..."
	$(RUNNER) black .
	$(RUNNER) ruff check --fix .

type-check: ## Run type checker
	@echo "Running type checker..."
	$(RUNNER) mypy src

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
	$(RUNNER) python -m {{ cookiecutter.project_slug }}.main

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
	$(RUNNER) pre-commit run --all-files

graph-install: ## Install graphify CLI (./scripts/install-graphify.sh)
	@./scripts/install-graphify.sh

graph: ## Build knowledge graph (graphify-out/)
	@command -v graphify >/dev/null 2>&1 || { echo "Run make graph-install first"; exit 1; }
	graphify extract .
	@echo "Open graphify-out/graph.html in a browser"

graph-update: ## Incrementally update graph after code changes (AST-only)
	@command -v graphify >/dev/null 2>&1 || { echo "Run make graph-install first"; exit 1; }
	@test -f graphify-out/graph.json || { echo "Run make graph first"; exit 1; }
	graphify update .

graph-query: ## Query graph: make graph-query QUERY="How does X work?"
	@command -v graphify >/dev/null 2>&1 || { echo "Run make graph-install first"; exit 1; }
	@test -n "$(QUERY)" || { echo 'Usage: make graph-query QUERY="your question"'; exit 1; }
	@test -f graphify-out/graph.json || { echo "Run make graph first"; exit 1; }
	graphify query "$(QUERY)"

