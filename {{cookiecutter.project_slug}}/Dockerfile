# dockerfile-utils: ignore
# Cookiecutter template: lines with Jinja2 template tags are not Docker instructions.
# Use Python 3.11 slim image as base
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# dockerfile-utils: ignore
{% if cookiecutter.dependency_manager == 'poetry' %}
COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root --no-interaction
# dockerfile-utils: ignore
{% else %}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# dockerfile-utils: ignore
{% endif %}

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (adjust as needed)
EXPOSE 8000

# Default command
CMD ["python", "-m", "{{ cookiecutter.project_slug }}.main"]

