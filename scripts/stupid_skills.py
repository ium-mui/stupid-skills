#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv or pip install needed):
#      uv run scripts/stupid_skills.py list
# 3. Or use the repository's Python:
#      python3 scripts/stupid_skills.py list
# ──────────────────

"""Discover, install, and synchronize skills in this repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import assert_never


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "repository.json"
SKILLS_START = "<!-- skills:start -->"
SKILLS_END = "<!-- skills:end -->"
VARIANTS_START = "<!-- variants:start -->"
VARIANTS_END = "<!-- variants:end -->"


@dataclass(frozen=True, slots=True)
class SkillRecord:
    name: str
    behavior: str
    locale: str
    description: str
    path: Path


@dataclass(frozen=True, slots=True)
class SkillNotFoundError(Exception):
    name: str

    def __str__(self) -> str:
        return f"unknown skill: {self.name}"


@dataclass(frozen=True, slots=True)
class CatalogFormatError(Exception):
    path: Path

    def __str__(self) -> str:
        return f"catalog markers are missing or out of order: {self.path}"


@dataclass(frozen=True, slots=True)
class FrontmatterFormatError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


class Command(StrEnum):
    LIST = "list"
    INSTALL = "install"
    SYNC = "sync"


def repository_tree_url(config_path: Path = CONFIG_PATH) -> str:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return str(config["repository_tree_url"]).rstrip("/")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, separator, raw_value = line.partition(":")
        valid_separator = separator == ":" and raw_value.startswith(" ")
        if not line or line.startswith((" ", "\t")) or not valid_separator:
            raise FrontmatterFormatError(
                message="frontmatter must use top-level key/value lines"
            )
        raw_value = raw_value.strip()
        normalized_key = key.strip()
        if (
            not normalized_key
            or normalized_key in values
            or not raw_value.startswith('"')
        ):
            raise FrontmatterFormatError(
                message=(
                    "frontmatter keys must be unique and values must be "
                    "JSON-quoted strings"
                )
            )
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError as error:
            message = f"invalid quoted frontmatter value: {error.msg}"
            raise FrontmatterFormatError(message=message) from error
        if not isinstance(value, str):
            raise FrontmatterFormatError(message="frontmatter values must be strings")
        values[normalized_key] = value
    return values


def discover_skills(skills_dir: Path = REPO_ROOT / "skills") -> tuple[SkillRecord, ...]:
    records: list[SkillRecord] = []
    for family_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        neutral_name = f"stupid-{family_dir.name}"
        locale_prefix = f"{neutral_name}-"
        for skill_dir in sorted(path for path in family_dir.iterdir() if path.is_dir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                continue
            frontmatter = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
            locale = (
                "neutral"
                if skill_dir.name == neutral_name
                else skill_dir.name.removeprefix(locale_prefix)
            )
            records.append(
                SkillRecord(
                    name=skill_dir.name,
                    behavior=family_dir.name,
                    locale=locale,
                    description=frontmatter.get("description", ""),
                    path=skill_dir,
                )
            )
    return tuple(records)


def install_command_for(behavior: str, name: str) -> str:
    url = repository_tree_url()
    return f"$skill-installer install {url}/skills/{behavior}/{name}"


def render_catalog(records: tuple[SkillRecord, ...], *, korean: bool) -> str:
    header = (
        "| 스킬 | 로케일 | 동작 | 설명 | 설치 |"
        if korean
        else "| Skill | Locale | Behavior | Description | Install |"
    )
    rows = [header, "| --- | --- | --- | --- | --- |"]
    rows.extend(
        f"| [`{record.name}`](skills/{record.behavior}/{record.name}) | "
        f"`{record.locale}` | `{record.behavior}` | {record.description} | "
        f"`{install_command_for(record.behavior, record.name)}` |"
        for record in records
    )
    return "\n".join(rows)


def replace_catalog(text: str, catalog: str, *, path: Path) -> str:
    start = text.find(SKILLS_START)
    end = text.find(SKILLS_END)
    if start == -1 or end == -1 or end < start:
        raise CatalogFormatError(path=path)
    content_start = start + len(SKILLS_START)
    return text[:content_start] + f"\n{catalog}\n" + text[end:]


def sync_family_catalog(family_dir: Path) -> None:
    variants = sorted(
        entry
        for entry in family_dir.iterdir()
        if entry.is_dir() and (entry / "SKILL.md").is_file()
    )
    catalog = "\n".join(
        f"- [`{variant.name}`]({variant.name}): "
        f"`{install_command_for(family_dir.name, variant.name)}`"
        for variant in variants
    )
    for filename in ("README.md", "README.ko.md"):
        path = family_dir / filename
        text = path.read_text(encoding="utf-8")
        start = text.find(VARIANTS_START)
        end = text.find(VARIANTS_END)
        if start == -1 or end == -1 or end < start:
            raise CatalogFormatError(path=path)
        content_start = start + len(VARIANTS_START)
        path.write_text(
            text[:content_start] + f"\n{catalog}\n" + text[end:],
            encoding="utf-8",
        )


def sync_root_catalogs(repository_root: Path, skills_dir: Path | None = None) -> None:
    readmes = (repository_root / "README.md", repository_root / "README.ko.md")
    present = tuple(path.is_file() for path in readmes)
    if not any(present):
        return
    if not all(present):
        missing = next(path for path in readmes if not path.is_file())
        raise CatalogFormatError(path=missing)

    records = discover_skills(skills_dir or repository_root / "skills")
    for path in readmes:
        rendered = render_catalog(records, korean=path.name.endswith(".ko.md"))
        path.write_text(
            replace_catalog(path.read_text(encoding="utf-8"), rendered, path=path),
            encoding="utf-8",
        )


def validate_root_catalogs(
    repository_root: Path,
    skills_dir: Path,
) -> list[str]:
    records = discover_skills(skills_dir)
    errors: list[str] = []
    for path in (repository_root / "README.md", repository_root / "README.ko.md"):
        if not path.is_file():
            errors.append(f"{path.name}: required top-level documentation is missing")
            continue
        expected = render_catalog(records, korean=path.name.endswith(".ko.md"))
        text = path.read_text(encoding="utf-8")
        try:
            synchronized = replace_catalog(text, expected, path=path)
        except CatalogFormatError as error:
            errors.append(str(error))
            continue
        if synchronized != text:
            errors.append(f"{path.name}: top-level skill catalog is stale")
    return errors


def install_skill(
    name: str,
    destination: Path,
    skills_dir: Path = REPO_ROOT / "skills",
) -> Path:
    record = next((item for item in discover_skills(skills_dir) if item.name == name), None)
    if record is None:
        raise SkillNotFoundError(name=name)
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / name
    if target.exists():
        raise FileExistsError(f"skill already exists: {target}")
    shutil.copytree(record.path, target)
    return target


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return Path(codex_home) / "skills" if codex_home else Path.home() / ".codex" / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir", type=Path, default=REPO_ROOT / "skills", help=argparse.SUPPRESS
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="list every installable skill")
    install_parser = subparsers.add_parser("install", help="install one skill")
    install_parser.add_argument("name", help="exact skill name from the list command")
    install_parser.add_argument(
        "--destination", type=Path, default=default_destination(), help="skills directory"
    )
    subparsers.add_parser("sync", help="synchronize top-level README catalogs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = Command(args.command)
    try:
        match command:
            case Command.LIST:
                for record in discover_skills(args.skills_dir):
                    print(
                        f"{record.name}\t{record.locale}\t{record.behavior}\t"
                        f"{record.description}"
                    )
            case Command.INSTALL:
                target = install_skill(args.name, args.destination, args.skills_dir)
                print(f"Installed {args.name} to {target}")
            case Command.SYNC:
                sync_root_catalogs(REPO_ROOT, args.skills_dir)
                print("Synchronized top-level skill catalogs.")
            case unreachable:
                assert_never(unreachable)
    except (
        CatalogFormatError,
        FileExistsError,
        FrontmatterFormatError,
        SkillNotFoundError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
