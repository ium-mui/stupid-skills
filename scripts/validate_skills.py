#!/usr/bin/env python3
"""Validate every installable skill against the stupid-skills rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "repository.json"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        raw_value = raw_value.strip()
        try:
            value = json.loads(raw_value) if raw_value.startswith('"') else raw_value.strip("'\"")
        except json.JSONDecodeError:
            value = raw_value.strip("'\"")
        values[key.strip()] = str(value)
    return values


def validate(skills_dir: Path, config_path: Path = CONFIG_PATH) -> list[str]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    prefix = f"{config['skill_prefix']}-"
    locales = sorted((str(item) for item in config["supported_locales"]), key=len, reverse=True)
    errors: list[str] = []

    if not skills_dir.is_dir():
        return [f"missing skills directory: {skills_dir}"]

    entries = sorted(skills_dir.iterdir())
    skill_dirs = [entry for entry in entries if entry.is_dir()]
    for entry in entries:
        if not entry.is_dir():
            errors.append(f"unexpected file directly under skills/: {entry.name}")

    if not skill_dirs:
        errors.append("skills/ must contain at least one skill directory")

    for skill_dir in skill_dirs:
        name = skill_dir.name
        label = f"{name}/SKILL.md"
        if len(name) > 63:
            errors.append(f"{name}: name must be shorter than 64 characters")
        if not NAME_PATTERN.fullmatch(name):
            errors.append(f"{name}: use lowercase letters, digits, and single hyphens only")
        if not name.startswith(prefix):
            errors.append(f"{name}: name must start with '{prefix}'")

        locale = next((item for item in locales if name.endswith(f"-{item}")), None)
        if locale is None:
            errors.append(f"{name}: name must end with a supported locale ({', '.join(locales)})")
        elif name == f"{prefix}{locale}":
            errors.append(f"{name}: behavior segment is missing")

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{label}: required file is missing")
            continue

        text = skill_file.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if not frontmatter:
            errors.append(f"{label}: valid YAML-style frontmatter is required")
            continue
        if frontmatter.get("name") != name:
            errors.append(f"{label}: frontmatter name must match the directory name")
        if not frontmatter.get("description", "").strip():
            errors.append(f"{label}: frontmatter description must not be empty")
        if "TODO" in text or "{{" in text or "}}" in text:
            errors.append(f"{label}: unfinished template markers are not allowed")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=REPO_ROOT / "skills")
    args = parser.parse_args()
    errors = validate(args.skills_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {len([item for item in args.skills_dir.iterdir() if item.is_dir()])} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
