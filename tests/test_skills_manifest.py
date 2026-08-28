"""Tests for skills-manifest.json and SKILLS_LOCK.json."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "scripts" / "skills-manifest.json"
TEMPLATE_ROOT = REPO_ROOT / "{{cookiecutter.project_slug}}"
LOCK_PATH = TEMPLATE_ROOT / "SKILLS_LOCK.json"

REQUIRED_SOURCE_FIELDS = {"id", "repo", "ref", "install"}
VALID_INSTALL_TYPES = {
    "full-tree",
    "ponytail",
    "allowlist",
    "composite",
    "rule-and-skill",
}


def _load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _target_skill_names(manifest: dict) -> list[str]:
    names: list[str] = []
    for source in manifest["sources"]:
        install_type = source["install"]["type"]
        rename = source.get("rename", {})
        skip_if_exists = set(source.get("skip_if_exists", []))
        if install_type in ("allowlist", "ponytail"):
            for skill in source.get("skills", []):
                target = rename.get(skill, skill)
                if target in skip_if_exists:
                    continue
                names.append(target)
        elif install_type == "full-tree":
            pass  # dynamic from upstream; checked separately via lock file
        elif install_type == "composite":
            for comp in source["install"].get("components", []):
                if "target_name" in comp:
                    names.append(comp["target_name"])
        elif install_type == "rule-and-skill":
            names.append(source["install"]["skill_target"])
    return names


def test_manifest_file_exists() -> None:
    assert MANIFEST_PATH.is_file()


def test_manifest_has_required_top_level_keys() -> None:
    manifest = _load_manifest()
    assert manifest["version"] == 1
    assert isinstance(manifest["preserve_local"], list)
    assert isinstance(manifest["sources"], list)
    assert len(manifest["sources"]) >= 10


def test_each_source_has_required_fields() -> None:
    manifest = _load_manifest()
    for source in manifest["sources"]:
        missing = REQUIRED_SOURCE_FIELDS - set(source.keys())
        assert not missing, f"{source.get('id')}: missing {missing}"
        assert source["install"]["type"] in VALID_INSTALL_TYPES


def test_allowlist_sources_have_skills_or_components() -> None:
    manifest = _load_manifest()
    for source in manifest["sources"]:
        install_type = source["install"]["type"]
        if install_type == "allowlist":
            assert source.get("skills"), f"{source['id']} allowlist missing skills"
        if install_type == "composite":
            assert source["install"].get("components"), f"{source['id']} composite missing components"


def test_no_duplicate_allowlist_target_names() -> None:
    manifest = _load_manifest()
    names = _target_skill_names(manifest)
    duplicates = {n for n in names if names.count(n) > 1}
    assert not duplicates, f"duplicate target skill names in manifest: {sorted(duplicates)}"


def test_preserve_local_skills_exist_in_template_or_are_local_only() -> None:
    manifest = _load_manifest()
    local_only = {"rtk-token-optimization", "awesome-agentic-patterns", "graphify"}
    for name in manifest["preserve_local"]:
        assert name in local_only, f"unexpected preserve_local entry: {name}"
        skill_dir = TEMPLATE_ROOT / ".cursor" / "skills" / name
        assert skill_dir.is_dir(), f"preserve_local skill missing in template: {name}"


def test_lock_file_exists_and_has_sources() -> None:
    assert LOCK_PATH.is_file()
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    assert "synced_at" in lock
    assert "sources" in lock
    assert len(lock["sources"]) >= 10


def test_lock_file_entries_have_sha_and_ref() -> None:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    for source_id, entry in lock["sources"].items():
        assert entry.get("ref"), f"{source_id} missing ref"
        assert entry.get("sha"), f"{source_id} missing sha"
        assert entry.get("repo"), f"{source_id} missing repo"


def test_template_has_communication_rules() -> None:
    karpathy = TEMPLATE_ROOT / ".cursor" / "rules" / "karpathy-guidelines.mdc"
    adhd = TEMPLATE_ROOT / ".cursor" / "rules" / "i-have-adhd.mdc"
    assert karpathy.is_file()
    assert adhd.is_file()
    assert "alwaysApply: true" in karpathy.read_text(encoding="utf-8")
    assert "alwaysApply: true" in adhd.read_text(encoding="utf-8")


def test_template_has_update_skills_assets() -> None:
    assert (TEMPLATE_ROOT / "scripts" / "skills-manifest.json").is_file()
    assert (TEMPLATE_ROOT / "scripts" / "update-skills.sh").is_file()
    assert (TEMPLATE_ROOT / "scripts" / "sync_skills.py").is_file()
    assert (TEMPLATE_ROOT / ".cursor" / "commands" / "update-skills.md").is_file()


def test_template_has_key_upstream_skills() -> None:
    expected = (
        "brainstorming",
        "grill-with-docs",
        "karpathy-guidelines",
        "i-have-adhd",
        "caveman",
        "taste-skill",
        "ui-ux-pro-max",
        "superpowers-test-driven-development",
        "mp-tdd",
    )
    skills_dir = TEMPLATE_ROOT / ".cursor" / "skills"
    for name in expected:
        assert (skills_dir / name / "SKILL.md").is_file(), f"missing skill: {name}"


def test_references_catalog_and_licenses_exist() -> None:
    catalog = TEMPLATE_ROOT / "references" / "skills-upstream-catalog.md"
    licenses = TEMPLATE_ROOT / "references" / "skills-licenses.md"
    assert catalog.is_file()
    assert licenses.is_file()
    assert "skills-manifest.json" in catalog.read_text(encoding="utf-8")
    assert "anthropics-skills" in licenses.read_text(encoding="utf-8")
