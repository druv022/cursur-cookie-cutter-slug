"""Tests for refreshing an existing generated project."""

from __future__ import annotations

from pathlib import Path

from cookiecutter.main import cookiecutter

from conftest import TEMPLATE_ROOT


def test_overwrite_existing_project(tmp_path: Path, cookiecutter_config: Path) -> None:
    """Re-running with overwrite_if_exists updates files instead of failing."""
    context = {
        "project_name": "Existing Project",
        "project_slug": "existing_project",
        "dependency_manager": "uv",
        "ci_cd": "github-actions",
        "use_docker": "y",
        "use_makefile": "y",
    }

    output_path = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context=context,
            config_file=str(cookiecutter_config),
        )
    )
    marker = output_path / ".cursor" / "commands" / "update-skills.md"
    assert marker.exists()
    original = marker.read_text(encoding="utf-8")

    marker.write_text("custom local change\n", encoding="utf-8")

    refreshed_path = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context=context,
            overwrite_if_exists=True,
            config_file=str(cookiecutter_config),
        )
    )

    assert refreshed_path == output_path
    refreshed = marker.read_text(encoding="utf-8")
    assert refreshed != "custom local change\n"
    assert "/update-skills" in refreshed
    assert refreshed == original
