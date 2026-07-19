"""Integration tests for dependency-manager template variants."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolated_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Isolate Cookiecutter state and the post-generation git identity."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Cookiecutter Tests")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "tests@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "Cookiecutter Tests")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "tests@example.com")


@pytest.fixture
def cookiecutter_config(tmp_path: Path) -> Path:
    """Create a Cookiecutter config whose caches stay in the test directory."""
    config_path = tmp_path / "cookiecutter-config.yaml"
    config_path.write_text(
        f"cookiecutters_dir: {tmp_path / 'templates'}\n"
        f"replay_dir: {tmp_path / 'replay'}\n",
        encoding="utf-8",
    )
    return config_path


@pytest.mark.parametrize(
    ("manager", "config_heading", "requirements_expected", "command"),
    [
        ("poetry", "[tool.poetry]", False, "poetry install"),
        ("uv", "[dependency-groups]", False, "uv sync"),
        ("pip", "[project.optional-dependencies]", True, "pip install -r requirements-dev.txt"),
        (
            "pip-tools",
            "[project.optional-dependencies]",
            True,
            "pip install -r requirements-dev.txt",
        ),
    ],
)
def test_dependency_manager_variant(
    tmp_path: Path,
    cookiecutter_config: Path,
    manager: str,
    config_heading: str,
    requirements_expected: bool,
    command: str,
) -> None:
    """Render each manager and verify its config, files, and commands."""
    project_slug = f"test_{manager.replace('-', '_')}"
    output_path = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "project_name": project_slug,
                "project_slug": project_slug,
                "dependency_manager": manager,
                "ci_cd": "github-actions",
                "use_docker": "y",
                "use_makefile": "y",
            },
            config_file=str(cookiecutter_config),
        )
    )

    pyproject_text = (output_path / "pyproject.toml").read_text(encoding="utf-8")
    pyproject = tomllib.loads(pyproject_text)
    readme = (output_path / "README.md").read_text(encoding="utf-8")

    assert pyproject
    assert config_heading in pyproject_text
    assert (output_path / "requirements.txt").exists() is requirements_expected
    assert (output_path / "requirements-dev.txt").exists() is requirements_expected
    assert command in readme
    assert "{{ cookiecutter.dependency_manager }}" not in pyproject_text


def test_uv_variant_uses_uv_across_development_surfaces(
    tmp_path: Path, cookiecutter_config: Path
) -> None:
    """Verify uv commands are rendered in local, Docker, and CI workflows."""
    output_path = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "project_name": "UV Project",
                "project_slug": "uv_project",
                "dependency_manager": "uv",
                "ci_cd": "github-actions",
                "use_docker": "y",
                "use_makefile": "y",
            },
            config_file=str(cookiecutter_config),
        )
    )

    makefile = (output_path / "Makefile").read_text(encoding="utf-8")
    dockerfile = (output_path / "Dockerfile").read_text(encoding="utf-8")
    workflow = (output_path / ".github/workflows/ci.yml").read_text(
        encoding="utf-8"
    )
    gitignore = (output_path / ".gitignore").read_text(encoding="utf-8")

    assert "RUNNER := uv run" in makefile
    assert "uv sync --no-dev" in makefile
    assert "pip install --no-cache-dir uv" in dockerfile
    assert "uv sync --no-dev" in dockerfile
    assert "uv sync" in workflow
    assert "uv run pytest" in workflow
    assert "uv export --no-dev" in workflow
    assert "uv.lock" not in gitignore


@pytest.mark.parametrize(
    ("ci_cd", "config_path"),
    [
        ("github-actions", ".github/workflows/ci.yml"),
        ("gitlab-ci", ".gitlab-ci.yml"),
        ("circleci", ".circleci/config.yml"),
    ],
)
def test_uv_variant_renders_selected_ci_pipeline(
    tmp_path: Path,
    cookiecutter_config: Path,
    ci_cd: str,
    config_path: str,
) -> None:
    """Verify every supported CI provider uses the uv environment."""
    project_slug = f"uv_{ci_cd.replace('-', '_')}"
    output_path = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "project_name": project_slug,
                "project_slug": project_slug,
                "dependency_manager": "uv",
                "ci_cd": ci_cd,
                "use_docker": "n",
                "use_makefile": "n",
            },
            config_file=str(cookiecutter_config),
        )
    )

    pipeline = (output_path / config_path).read_text(encoding="utf-8")

    assert "uv sync" in pipeline
    assert "uv run" in pipeline
    assert "uv export --no-dev" in pipeline


@pytest.mark.parametrize(
    ("manager", "install_command"),
    [
        ("poetry", "pip install poetry bandit safety"),
        ("uv", "pip install uv bandit safety"),
    ],
)
def test_gitlab_security_bandit_runs_from_pip_environment(
    tmp_path: Path, cookiecutter_config: Path, manager: str, install_command: str
) -> None:
    """Ensure GitLab security job installs and executes Bandit consistently."""
    output_path = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "project_name": f"security_{manager}",
                "project_slug": f"security_{manager}",
                "dependency_manager": manager,
                "ci_cd": "gitlab-ci",
                "use_docker": "n",
                "use_makefile": "n",
            },
            config_file=str(cookiecutter_config),
        )
    )

    pipeline = (output_path / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert install_command in pipeline
    assert "\n    - bandit -r . -ll\n" in pipeline
    assert "poetry run bandit -r . -ll" not in pipeline
    assert "uv run --with bandit bandit -r . -ll" not in pipeline
