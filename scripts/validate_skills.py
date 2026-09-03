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
FAMILY_DOCS = {"README.md", "README.ko.md"}
VARIANTS_START = "<!-- variants:start -->"
VARIANTS_END = "<!-- variants:end -->"


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
    locales = {str(item) for item in config["supported_locales"]}
    errors: list[str] = []

    if not skills_dir.is_dir():
        return [f"missing skills directory: {skills_dir}"]

    root_entries = sorted(skills_dir.iterdir())
    family_dirs = [entry for entry in root_entries if entry.is_dir()]
    for entry in root_entries:
        if not entry.is_dir():
            errors.append(f"unexpected file directly under skills/: {entry.name}")

    if not family_dirs:
        errors.append("skills/ must contain at least one behavior family")

    for family_dir in family_dirs:
        family = family_dir.name
        if not NAME_PATTERN.fullmatch(family):
            errors.append(f"{family}: family names must use lowercase letters, digits, and single hyphens")
        if family.startswith(prefix):
            errors.append(f"{family}: family names must not include the '{prefix}' prefix")

        family_entries = sorted(family_dir.iterdir())
        skill_dirs = [entry for entry in family_entries if entry.is_dir()]
        for entry in family_entries:
            if entry.is_file() and entry.name not in FAMILY_DOCS:
                errors.append(f"{family}/{entry.name}: unexpected file at the family level")
        for filename in sorted(FAMILY_DOCS):
            family_doc = family_dir / filename
            if not family_doc.is_file():
                errors.append(f"{family}/{filename}: required family documentation is missing")
        if not skill_dirs:
            errors.append(f"{family}: family must contain at least one installable skill")

        for skill_dir in skill_dirs:
            name = skill_dir.name
            label = f"{family}/{name}/SKILL.md"
            if len(name) > 63:
                errors.append(f"{family}/{name}: name must be shorter than 64 characters")
            if not NAME_PATTERN.fullmatch(name):
                errors.append(f"{family}/{name}: use lowercase letters, digits, and single hyphens only")

            localized_names = {f"{prefix}{family}-{locale}" for locale in locales}
            language_neutral_name = f"{prefix}{family}"
            if name != language_neutral_name and name not in localized_names:
                choices = ", ".join(sorted(locales))
                errors.append(
                    f"{family}/{name}: expected '{language_neutral_name}' or "
                    f"'{prefix}{family}-<locale>' with one of: {choices}"
                )

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
                errors.append(f"{label}: frontmatter name must match the skill directory name")
            if not frontmatter.get("description", "").strip():
                errors.append(f"{label}: frontmatter description must not be empty")
            if "TODO" in text or "{{" in text or "}}" in text:
                errors.append(f"{label}: unfinished template markers are not allowed")

        for filename in sorted(FAMILY_DOCS):
            family_doc = family_dir / filename
            if not family_doc.is_file():
                continue
            text = family_doc.read_text(encoding="utf-8")
            if not text.strip():
                errors.append(f"{family}/{filename}: family documentation must not be empty")
            if VARIANTS_START not in text or VARIANTS_END not in text:
                errors.append(f"{family}/{filename}: variant catalog markers are required")
            else:
                start = text.find(VARIANTS_START) + len(VARIANTS_START)
                end = text.find(VARIANTS_END, start)
                actual_catalog = text[start:end].strip()
                expected_catalog = "\n".join(
                    f"- [`{skill_dir.name}`]({skill_dir.name})"
                    for skill_dir in sorted(skill_dirs)
                )
                if actual_catalog != expected_catalog:
                    errors.append(
                        f"{family}/{filename}: variant catalog must exactly match skill directories"
                    )
            if "TODO" in text or "{{" in text or "}}" in text:
                errors.append(f"{family}/{filename}: unfinished template markers are not allowed")

    return errors


def count_skills(skills_dir: Path) -> int:
    return sum(
        1
        for family in skills_dir.iterdir()
        if family.is_dir()
        for skill in family.iterdir()
        if skill.is_dir()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=REPO_ROOT / "skills")
    args = parser.parse_args()
    errors = validate(args.skills_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {count_skills(args.skills_dir)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
