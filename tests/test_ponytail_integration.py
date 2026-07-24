"""Integration tests for ponytail vendoring in generated projects."""

from __future__ import annotations

from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

from conftest import TEMPLATE_ROOT

PONYTAIL_SKILLS = (
    "ponytail",
    "ponytail-audit",
    "ponytail-debt",
    "ponytail-gain",
    "ponytail-help",
    "ponytail-review",
)

PONYTAIL_COMMANDS = (
    "ponytail.md",
    "ponytail-audit.md",
    "ponytail-debt.md",
    "ponytail-gain.md",
    "ponytail-help.md",
    "ponytail-review.md",
)


def _generate_project(
    tmp_path: Path,
    cookiecutter_config: Path,
    *,
    project_slug: str = "ponytail_project",
    dependency_manager: str = "uv",
) -> Path:
    return Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "project_name": project_slug,
                "project_slug": project_slug,
                "dependency_manager": dependency_manager,
                "ci_cd": "github-actions",
                "use_docker": "y",
                "use_makefile": "y",
            },
            config_file=str(cookiecutter_config),
        )
    )


def _assert_ponytail_assets(output_path: Path) -> None:
    rule_path = output_path / ".cursor/rules/ponytail.mdc"
    assert rule_path.is_file(), "missing always-on ponytail rule"
    rule_text = rule_path.read_text(encoding="utf-8")
    assert "alwaysApply: true" in rule_text
    assert "YAGNI" in rule_text

    version_path = output_path / "PONYTAIL_VERSION"
    assert version_path.is_file(), "missing PONYTAIL_VERSION pin file"
    version_text = version_path.read_text(encoding="utf-8")
    assert "ref=" in version_text
    assert "sha=" in version_text
    assert "source=https://github.com/DietrichGebert/ponytail.git" in version_text

    for skill in PONYTAIL_SKILLS:
        skill_path = output_path / ".cursor/skills" / skill / "SKILL.md"
        assert skill_path.is_file(), f"missing ponytail skill: {skill}"
        assert skill_path.read_text(encoding="utf-8").strip()

    commands_dir = output_path / ".cursor/commands"
    for command in PONYTAIL_COMMANDS:
        command_path = commands_dir / command
        assert command_path.is_file(), f"missing ponytail command: {command}"
        command_text = command_path.read_text(encoding="utf-8")
        assert "{{" not in command_text, f"unescaped Jinja in {command}"
        assert "ponytail" in command_text.lower()

    agent_skills = (
        output_path / ".cursor/rules/agent-skills.mdc"
    ).read_text(encoding="utf-8")
    assert "ponytail.mdc" in agent_skills
    assert "/ponytail-review" in agent_skills

    cursor_docs = (
        output_path / "docs/CURSOR_AGENT_SKILLS.md"
    ).read_text(encoding="utf-8")
    assert "Ponytail" in cursor_docs
    assert "/ponytail-review" in cursor_docs

    readme = (output_path / "README.md").read_text(encoding="utf-8")
    assert "PONYTAIL_VERSION" in readme
    assert "/ponytail" in readme


@pytest.mark.parametrize(
    "dependency_manager",
    ["poetry", "uv", "pip", "pip-tools"],
)
def test_ponytail_assets_present_for_dependency_manager(
    tmp_path: Path,
    cookiecutter_config: Path,
    dependency_manager: str,
) -> None:
    """Every dependency-manager variant should ship ponytail rule, skills, and commands."""
    project_slug = f"ponytail_{dependency_manager.replace('-', '_')}"
    output_path = _generate_project(
        tmp_path,
        cookiecutter_config,
        project_slug=project_slug,
        dependency_manager=dependency_manager,
    )
    _assert_ponytail_assets(output_path)


def test_ponytail_command_references_skill(
    tmp_path: Path, cookiecutter_config: Path
) -> None:
    """Ponytail slash commands should route to the matching skill file."""
    output_path = _generate_project(tmp_path, cookiecutter_config)
    review_cmd = (
        output_path / ".cursor/commands/ponytail-review.md"
    ).read_text(encoding="utf-8")
    assert ".cursor/skills/ponytail-review/SKILL.md" in review_cmd


def test_ponytail_mode_command_describes_levels(
    tmp_path: Path, cookiecutter_config: Path
) -> None:
    """The /ponytail command should document intensity levels without raw {{args}}."""
    output_path = _generate_project(tmp_path, cookiecutter_config)
    mode_cmd = (output_path / ".cursor/commands/ponytail.md").read_text(
        encoding="utf-8"
    )
    assert "lite" in mode_cmd
    assert "full" in mode_cmd
    assert "ultra" in mode_cmd
    assert "off" in mode_cmd
    assert "{{" not in mode_cmd
