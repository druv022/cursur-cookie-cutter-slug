#!/usr/bin/env python3
"""Sync agent skills from upstream GitHub repos per skills-manifest.json."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def clone_repo(repo: str, ref: str, dest: Path) -> tuple[str, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    try:
        run(["git", "clone", "--depth", "1", "--branch", ref, repo, str(dest)])
        resolved_ref = ref
    except subprocess.CalledProcessError:
        if dest.exists():
            shutil.rmtree(dest)
        run(["git", "clone", "--depth", "1", "--branch", "main", repo, str(dest)])
        resolved_ref = "main"
    sha = run(["git", "-C", str(dest), "rev-parse", "HEAD"]).stdout.strip()
    describe = run(
        ["git", "-C", str(dest), "describe", "--tags", "--always"],
        check=False,
    ).stdout.strip() or sha
    return resolved_ref, sha, describe


def escape_cookiecutter_braces(text: str) -> str:
    return text.replace("{{", "{ {").replace("}}", "} }")


def adapt_claude_command(content: str) -> str:
    content = re.sub(
        r"Invoke the agent-skills:([a-z0-9-]+) skill\.",
        r"Read and follow `.cursor/skills/\1/SKILL.md`.",
        content,
    )
    content = re.sub(
        r"agent-skills:([a-z0-9-]+)",
        r".cursor/skills/\1/SKILL.md",
        content,
    )
    content = re.sub(
        r"superpowers:([a-z0-9-]+)",
        r".cursor/skills/\1/SKILL.md",
        content,
    )
    return content


def toml_to_cursor_cmd(toml_file: Path, out_file: Path, skill_name: str) -> None:
    text = toml_file.read_text(encoding="utf-8")
    desc_match = re.search(r'^description\s*=\s*"([^"]*)"', text, re.M)
    prompt_match = re.search(r'^prompt\s*=\s*"([^"]*)"', text, re.M)
    description = desc_match.group(1) if desc_match else ""
    prompt = prompt_match.group(1) if prompt_match else ""
    prompt = prompt.replace("{{args}}", "the level the user provided (lite, full, ultra, or off)")
    body = (
        f"---\ndescription: {description}\n---\n\n"
        f"Read and follow `.cursor/skills/{skill_name}/SKILL.md`.\n\n"
        f"{prompt}\n"
    )
    out_file.write_text(body, encoding="utf-8")


def target_name(source_id: str, skill: str, rename: dict[str, str]) -> str:
    return rename.get(skill, skill)


def skill_exists(project_root: Path, name: str) -> bool:
    return (project_root / ".cursor" / "skills" / name).exists()


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def install_allowlist_skill(
    repo_root: Path,
    skills_path: str,
    skill: str,
    project_root: Path,
    rename: dict[str, str],
    skip_if_exists: list[str],
    installed: set[str],
) -> str | None:
    target = target_name("", skill, rename)
    if target in skip_if_exists and skill_exists(project_root, target):
        return None
    if target in installed:
        raise RuntimeError(f"Duplicate skill target name: {target}")
    src = repo_root / skills_path / skill
    if not src.is_dir():
        alt = repo_root / skill
        if alt.is_dir():
            src = alt
        else:
            raise FileNotFoundError(f"Skill not found: {skill} under {skills_path}")
    dst = project_root / ".cursor" / "skills" / target
    copy_tree(src, dst)
    installed.add(target)
    return target


class SkillsSyncer:
    def __init__(self, project_root: Path, manifest_path: Path, source_filter: str | None = None):
        self.project_root = project_root.resolve()
        self.manifest_path = manifest_path.resolve()
        self.source_filter = source_filter
        self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.tmp = Path(subprocess.check_output(["mktemp", "-d"], text=True).strip())
        self.lock: dict[str, Any] = {"synced_at": "", "sources": {}}
        self.installed_skills: set[str] = set()
        self.preserve_local = self.manifest.get("preserve_local", [])

    def cleanup(self) -> None:
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def backup_preserve_local(self) -> Path:
        backup = self.tmp / "preserve-local"
        backup.mkdir(parents=True)
        skills_dir = self.project_root / ".cursor" / "skills"
        for name in self.preserve_local:
            src = skills_dir / name
            if src.is_dir():
                copy_tree(src, backup / name)
        return backup

    def restore_preserve_local(self, backup: Path) -> None:
        skills_dir = self.project_root / ".cursor" / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        for name in self.preserve_local:
            src = backup / name
            if src.is_dir():
                copy_tree(src, skills_dir / name)

    def ensure_dirs(self) -> None:
        for rel in [".cursor/skills", ".cursor/rules", ".cursor/commands", ".cursor/agents", "references", "scripts"]:
            (self.project_root / rel).mkdir(parents=True, exist_ok=True)

    def sync_addyosmani(self, source: dict[str, Any], repo_root: Path) -> list[str]:
        install = source["install"]
        skills_src = repo_root / install["skills_path"]
        skills_dst = self.project_root / ".cursor" / "skills"
        skills_dst.mkdir(parents=True, exist_ok=True)
        synced: list[str] = []
        exclude = set(self.preserve_local)
        for item in skills_src.iterdir():
            if not item.is_dir():
                continue
            if item.name in exclude:
                continue
            dst = skills_dst / item.name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(item, dst)
            self.installed_skills.add(item.name)
            synced.append(item.name)
        refs_src = repo_root / install.get("references_path", "references")
        if refs_src.is_dir():
            refs_dst = self.project_root / "references"
            for f in refs_src.glob("*.md"):
                shutil.copy2(f, refs_dst / f.name)
        agents_src = repo_root / install.get("agents_path", "agents")
        if agents_src.is_dir():
            agents_dst = self.project_root / ".cursor" / "agents"
            for f in agents_src.glob("*.md"):
                shutil.copy2(f, agents_dst / f.name)
        cmd_src = repo_root / install.get("commands_path", ".claude/commands")
        if cmd_src.is_dir():
            cmd_dst = self.project_root / ".cursor" / "commands"
            for f in cmd_src.glob("*.md"):
                content = adapt_claude_command(f.read_text(encoding="utf-8"))
                (cmd_dst / f.name).write_text(content, encoding="utf-8")
        return synced

    def sync_ponytail(self, source: dict[str, Any], repo_root: Path) -> list[str]:
        install = source["install"]
        rule_src = repo_root / install["rules_path"]
        rule_dst = self.project_root / ".cursor" / "rules" / "ponytail.mdc"
        shutil.copy2(rule_src, rule_dst)
        synced: list[str] = []
        glob_prefix = install.get("skills_glob", "skills/ponytail")
        for skill_dir in (repo_root / "skills").glob("ponytail*"):
            if not skill_dir.is_dir():
                continue
            name = skill_dir.name
            dst = self.project_root / ".cursor" / "skills" / name
            copy_tree(skill_dir, dst)
            self.installed_skills.add(name)
            synced.append(name)
        cmd_src = repo_root / install.get("commands_path", "commands")
        if cmd_src.is_dir():
            for toml_file in cmd_src.glob("*.toml"):
                base = toml_file.stem
                skill = "ponytail" if base == "ponytail" else base
                toml_to_cursor_cmd(
                    toml_file,
                    self.project_root / ".cursor" / "commands" / f"{base}.md",
                    skill,
                )
        return synced

    def sync_allowlist(self, source: dict[str, Any], repo_root: Path) -> list[str]:
        install = source["install"]
        rename = source.get("rename", {})
        skip_if = source.get("skip_if_exists", []) + self.manifest.get("skip_if_exists", [])
        synced: list[str] = []
        for skill in source.get("skills", []):
            if skill in source.get("skip", []):
                continue
            result = install_allowlist_skill(
                repo_root,
                install["skills_path"],
                skill,
                self.project_root,
                rename,
                skip_if,
                self.installed_skills,
            )
            if result:
                synced.append(result)
        for extra in source.get("extra_paths", []):
            src = repo_root / extra["source"]
            dst = self.project_root / extra["target"]
            if src.is_dir():
                copy_tree(src, dst)
        return synced

    def sync_composite(self, source: dict[str, Any], repo_root: Path) -> list[str]:
        synced: list[str] = []
        for comp in source["install"].get("components", []):
            src = repo_root / comp["source_path"]
            if "target_name" in comp:
                dst = self.project_root / ".cursor" / "skills" / comp["target_name"]
                copy_tree(src, dst)
                self.installed_skills.add(comp["target_name"])
                synced.append(comp["target_name"])
            elif "target_path" in comp:
                dst = self.project_root / comp["target_path"]
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        return synced

    def sync_rule_and_skill(self, source: dict[str, Any], repo_root: Path) -> list[str]:
        install = source["install"]
        synced: list[str] = []
        rule_src = repo_root / install["rule_source"] if install.get("rule_source") else None
        rule_dst = self.project_root / install["rule_target"]
        rule_dst.parent.mkdir(parents=True, exist_ok=True)

        skill_src = repo_root / install["skill_source"]
        if not skill_src.is_dir():
            alt = repo_root / "skills" / install["skill_target"]
            if alt.is_dir():
                skill_src = alt
        if not skill_src.is_dir():
            raise FileNotFoundError(f"Skill not found for {source['id']}: {install['skill_source']}")

        if rule_src and rule_src.is_file():
            content = rule_src.read_text(encoding="utf-8")
            if "alwaysApply:" not in content:
                content = content.replace("---\n", "---\nalwaysApply: true\n", 1)
            rule_dst.write_text(content, encoding="utf-8")
        else:
            rule_dst.write_text(self._generated_always_on_rule(install["skill_target"]), encoding="utf-8")

        skill_name = install["skill_target"]
        skill_dst = self.project_root / ".cursor" / "skills" / skill_name
        copy_tree(skill_src, skill_dst)
        self.installed_skills.add(skill_name)
        synced.append(skill_name)
        return synced

    def _generated_always_on_rule(self, skill_name: str) -> str:
        if skill_name == "i-have-adhd":
            return """---
description: ADHD-friendly agent output — action first, numbered steps, no preamble
alwaysApply: true
---

# i-have-adhd output rules

Apply on every response (see `.cursor/skills/i-have-adhd/SKILL.md` for full detail):

1. Lead with the next action the reader can take now.
2. Number multi-step tasks; one bounded action per step.
3. End with one concrete next step if anything remains open.
4. Suppress tangents until the current task is done.
5. Restate progress each turn (e.g. "Step 3 of 5 done").
6. Use specific time estimates in minutes or hours, not "a bit."
7. Make completed wins visible in concrete terms.
8. Matter-of-fact errors: cause + fix, no "Uh oh."
9. Cap lists at five items; split into now vs later if needed.
10. No preamble, no recap, no "Hope this helps" closers.

Stack with Karpathy and ponytail: think first and stay minimal, but format for action.
"""
        return f"""---
description: Always-on guidance from {skill_name}
alwaysApply: true
---

Read and follow `.cursor/skills/{skill_name}/SKILL.md` when relevant.
"""

    def write_template_commands(self) -> None:
        for cmd in self.manifest.get("template_commands", []):
            if cmd.get("script"):
                continue
            path = self.project_root / ".cursor" / "commands" / f"{cmd['name']}.md"
            body = (
                f"---\ndescription: {cmd['description']}\n---\n\n"
                f"Read and follow `.cursor/skills/{cmd['skill']}/SKILL.md`.\n"
            )
            path.write_text(body, encoding="utf-8")

    def write_update_skills_command(self) -> None:
        path = self.project_root / ".cursor" / "commands" / "update-skills.md"
        body = (
            "---\n"
            "description: Re-vendor agent skills from upstream GitHub repos per scripts/skills-manifest.json\n"
            "---\n\n"
            "Run `./scripts/update-skills.sh` from the project root. "
            "Review `git diff` for skill changes. Read `SKILLS_LOCK.json` for pinned SHAs. "
            "Do not commit unless the user asks.\n"
        )
        path.write_text(body, encoding="utf-8")

    def write_reference_catalog(self) -> None:
        lines = [
            "# Upstream skills catalog (reference)",
            "",
            "This project vendors a **curated subset** of skills from upstream repositories.",
            "To add more skills, edit `scripts/skills-manifest.json` and run `./scripts/update-skills.sh`.",
            "",
            "## Vendored sources",
            "",
        ]
        for source in self.manifest["sources"]:
            lines.append(f"- **{source['id']}**: {source['repo']} ({source.get('license_note', '')})")
        lines.extend(["", "## Full upstream catalogs (not all vendored)", ""])
        for cat in self.manifest.get("reference_catalogs", []):
            lines.append(f"- [{cat['id']}]({cat['repo']}): {cat['description']}")
        lines.extend(["", "## License notes", ""])
        lines.append("See [skills-licenses.md](skills-licenses.md) for per-source license details.")
        (self.project_root / "references" / "skills-upstream-catalog.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    def write_licenses(self) -> None:
        lines = [
            "# Skills upstream licenses",
            "",
            "| Source | License | Notes |",
            "|--------|---------|-------|",
        ]
        for source in self.manifest["sources"]:
            note = source.get("license_note", "")
            lines.append(f"| [{source['id']}]({source['repo']}) | {note.split(';')[0]} | {note} |")
        lines.extend([
            "",
            "## Not vendored",
            "",
            "Anthropic document skills (`docx`, `pdf`, `pptx`, `xlsx`) are source-available only and are excluded from this template.",
            "",
        ])
        (self.project_root / "references" / "skills-licenses.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    def write_lock_and_legacy_versions(self) -> None:
        self.lock["synced_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        lock_path = self.project_root / "SKILLS_LOCK.json"
        lock_path.write_text(json.dumps(self.lock, indent=2) + "\n", encoding="utf-8")
        agent = self.lock["sources"].get("addyosmani-agent-skills")
        if agent:
            self._write_legacy_version("AGENT_SKILLS_VERSION", agent)
        pony = self.lock["sources"].get("ponytail")
        if pony:
            self._write_legacy_version("PONYTAIL_VERSION", pony)

    def _write_legacy_version(self, filename: str, entry: dict[str, Any]) -> None:
        path = self.project_root / filename
        body = (
            f"ref={entry['ref']}\n"
            f"sha={entry['sha']}\n"
            f"describe={entry.get('describe', entry['sha'])}\n"
            f"source={entry['repo']}\n"
            f"synced_at={self.lock['synced_at']}\n"
            f"# Deprecated: see SKILLS_LOCK.json\n"
        )
        path.write_text(body, encoding="utf-8")

    def copy_manifest_to_project(self, manifest_src: Path) -> None:
        dst = self.project_root / "scripts" / "skills-manifest.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manifest_src, dst)

    def sync_source(self, source: dict[str, Any]) -> None:
        source_id = source["id"]
        if self.source_filter and source_id != self.source_filter:
            return
        print(f"Syncing {source_id} @ {source['ref']} ...")
        clone_dest = self.tmp / "repos" / source_id
        ref, sha, describe = clone_repo(source["repo"], source["ref"], clone_dest)
        install_type = source["install"]["type"]
        if install_type == "full-tree":
            synced = self.sync_addyosmani(source, clone_dest)
        elif install_type == "ponytail":
            synced = self.sync_ponytail(source, clone_dest)
        elif install_type == "allowlist":
            synced = self.sync_allowlist(source, clone_dest)
        elif install_type == "composite":
            synced = self.sync_composite(source, clone_dest)
        elif install_type == "rule-and-skill":
            synced = self.sync_rule_and_skill(source, clone_dest)
        else:
            raise ValueError(f"Unknown install type: {install_type}")
        self.lock["sources"][source_id] = {
            "ref": ref,
            "sha": sha,
            "describe": describe,
            "repo": source["repo"],
            "skills": synced,
            "skill_count": len(synced),
        }
        print(f"  synced {len(synced)} skill(s): {', '.join(synced[:5])}{'...' if len(synced) > 5 else ''}")

    def run(self, manifest_src: Path | None = None) -> None:
        try:
            self.ensure_dirs()
            backup = self.backup_preserve_local()
            for source in self.manifest["sources"]:
                self.sync_source(source)
            self.restore_preserve_local(backup)
            if not self.source_filter:
                self.write_template_commands()
                self.write_update_skills_command()
                self.write_reference_catalog()
                self.write_licenses()
                if manifest_src:
                    self.copy_manifest_to_project(manifest_src)
                self.write_lock_and_legacy_versions()
            skill_count = len(list((self.project_root / ".cursor" / "skills").iterdir()))
            print(f"\nDone. {skill_count} skills under .cursor/skills/")
            print(f"Wrote {self.project_root / 'SKILLS_LOCK.json'}")
        finally:
            self.cleanup()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync agent skills from upstream repos")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Target project root (default: auto-detect)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to skills-manifest.json",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Sync only this source id",
    )
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    manifest_path = args.manifest or (script_dir / "skills-manifest.json")
    if args.project_root:
        project_root = args.project_root
    else:
        template_dir = repo_root / "{{cookiecutter.project_slug}}"
        project_root = template_dir if template_dir.is_dir() else Path.cwd()
    syncer = SkillsSyncer(project_root, manifest_path, source_filter=args.source)
    syncer.run(manifest_src=manifest_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
