"""Shared fixtures for cookiecutter template integration tests."""

from __future__ import annotations

from pathlib import Path

import pytest

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
