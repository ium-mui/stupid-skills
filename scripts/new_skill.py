#!/usr/bin/env python3
"""Create one stupid skill and maintain its bilingual family documentation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "repository.json"
TEMPLATE_PATH = REPO_ROOT / "templates" / "SKILL.md.template"
FAMILY_TEMPLATE_EN = REPO_ROOT / "templates" / "FAMILY_README.md.template"
FAMILY_TEMPLATE_KO = REPO_ROOT / "templates" / "FAMILY_README.ko.md.template"
VARIANTS_START = "<!-- variants:start -->"
VARIANTS_END = "<!-- variants:end -->"


def load_config(path: Path = CONFIG_PATH) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def one_line(value: str) -> str:
    return " ".join(value.split())


def blockquote(value: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in value.splitlines())


def replace_markers(template: str, replacements: dict[str, str]) -> str:
    rendered = template
    for marker, value in replacements.items():
        rendered = rendered.replace(marker, value)
    if "{{" in rendered or "}}" in rendered:
        raise RuntimeError("a template contains an unresolved marker")
    return rendered


def replace_variant_catalog(text: str, catalog: str) -> str:
    start = text.find(VARIANTS_START)
    end = text.find(VARIANTS_END)
    if start == -1 or end == -1 or end < start:
        raise RuntimeError("family README is missing variant catalog markers")
    content_start = start + len(VARIANTS_START)
    return text[:content_start] + f"\n{catalog}\n" + text[end:]


def update_family_catalog(family_dir: Path) -> None:
    variants = sorted(
        entry.name
        for entry in family_dir.iterdir()
        if entry.is_dir() and (entry / "SKILL.md").is_file()
    )
    catalog = "\n".join(f"- [`{name}`]({name})" for name in variants)
    for filename in ("README.md", "README.ko.md"):
        path = family_dir / filename
        path.write_text(
            replace_variant_catalog(path.read_text(encoding="utf-8"), catalog),
            encoding="utf-8",
        )


def create_skill(
    *,
    behavior: str,
    locale: str | None,
    description: str,
    instructions: list[str],
    example_input: str,
    example_output: str,
    title: str | None = None,
    family_description_en: str | None = None,
    family_description_ko: str | None = None,
    skills_dir: Path | None = None,
    config_path: Path = CONFIG_PATH,
    template_path: Path = TEMPLATE_PATH,
    family_template_en: Path = FAMILY_TEMPLATE_EN,
    family_template_ko: Path = FAMILY_TEMPLATE_KO,
) -> Path:
    config = load_config(config_path)
    prefix = str(config["skill_prefix"])
    supported_locales = {str(item) for item in config["supported_locales"]}

    behavior_slug = slugify(behavior)
    locale_slug = locale.strip().lower() if locale is not None else None
    if not behavior_slug:
        raise ValueError("behavior must contain at least one ASCII letter or digit")
    if locale_slug is not None and locale_slug not in supported_locales:
        choices = ", ".join(sorted(supported_locales))
        raise ValueError(f"unsupported locale '{locale_slug}'; choose one of: {choices}")
    if not one_line(description):
        raise ValueError("description must not be empty")
    cleaned_instructions = [one_line(item) for item in instructions if one_line(item)]
    if not cleaned_instructions:
        raise ValueError("at least one instruction is required")
    if not example_input.strip() or not example_output.strip():
        raise ValueError("example input and output must not be empty")

    skill_name = (
        f"{prefix}-{behavior_slug}-{locale_slug}"
        if locale_slug is not None
        else f"{prefix}-{behavior_slug}"
    )
    if len(skill_name) > 63:
        raise ValueError("generated skill name must be shorter than 64 characters")

    target_root = skills_dir or REPO_ROOT / "skills"
    family_dir = target_root / behavior_slug
    target = family_dir / skill_name
    if target.exists():
        raise FileExistsError(f"skill already exists: {target}")

    display_title = one_line(title) if title else behavior_slug.replace("-", " ").title()
    if family_dir.exists():
        for filename in ("README.md", "README.ko.md"):
            if not (family_dir / filename).is_file():
                raise RuntimeError(f"existing family is missing {filename}: {family_dir}")
    else:
        description_en = one_line(family_description_en or "")
        description_ko = one_line(family_description_ko or "")
        if not description_en or not description_ko:
            raise ValueError(
                "new families require English and Korean family descriptions"
            )
        family_dir.mkdir(parents=True)
        family_replacements = {
            "{{TITLE}}": display_title,
            "{{FAMILY_DESCRIPTION_EN}}": description_en,
            "{{FAMILY_DESCRIPTION_KO}}": description_ko,
        }
        (family_dir / "README.md").write_text(
            replace_markers(
                family_template_en.read_text(encoding="utf-8"), family_replacements
            ),
            encoding="utf-8",
        )
        (family_dir / "README.ko.md").write_text(
            replace_markers(
                family_template_ko.read_text(encoding="utf-8"), family_replacements
            ),
            encoding="utf-8",
        )

    instruction_markdown = "\n".join(f"- {item}" for item in cleaned_instructions)
    description_text = one_line(description)
    locale_label = locale_slug or "language-neutral"
    locale_rule = (
        f"- Keep this skill fixed to locale `{locale_slug}`; never detect or switch locale automatically."
        if locale_slug is not None
        else "- Keep this skill language-neutral; do not add locale-specific behavior."
    )
    replacements = {
        "{{SKILL_NAME_YAML}}": json.dumps(skill_name, ensure_ascii=False),
        "{{DESCRIPTION_YAML}}": json.dumps(description_text, ensure_ascii=False),
        "{{TITLE}}": display_title,
        "{{LOCALE_LABEL}}": locale_label,
        "{{LOCALE_RULE}}": locale_rule,
        "{{DESCRIPTION_TEXT}}": description_text,
        "{{INSTRUCTIONS}}": instruction_markdown + "\n",
        "{{EXAMPLE_INPUT}}": blockquote(example_input.strip()),
        "{{EXAMPLE_OUTPUT}}": blockquote(example_output.strip()),
    }

    rendered = replace_markers(template_path.read_text(encoding="utf-8"), replacements)

    target.mkdir(parents=True)
    output = target / "SKILL.md"
    output.write_text(rendered, encoding="utf-8")
    update_family_catalog(family_dir)
    return output


def prompt_value(current: str | None, label: str, default: str | None = None) -> str:
    if current is not None:
        return current
    if not sys.stdin.isatty():
        if default is not None:
            return default
        raise ValueError(f"missing required option: {label}")
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def collect_instructions(current: list[str] | None) -> list[str]:
    if current:
        return current
    if not sys.stdin.isatty():
        raise ValueError("provide at least one --instruction")
    print("Instructions (enter a blank line when finished):")
    values: list[str] = []
    while True:
        value = input(f"  {len(values) + 1}. ").strip()
        if not value:
            break
        values.append(value)
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--behavior", help="ASCII behavior slug, such as kkwettu")
    locale_group = parser.add_mutually_exclusive_group()
    locale_group.add_argument("--locale", help="supported locale, such as en-us or ko")
    locale_group.add_argument(
        "--language-neutral",
        action="store_true",
        help="create a skill without a locale suffix",
    )
    parser.add_argument("--title", help="human-readable skill title")
    parser.add_argument("--description", help="one-line discovery description")
    parser.add_argument("--family-description-en", help="new family description in English")
    parser.add_argument("--family-description-ko", help="new family description in Korean")
    parser.add_argument(
        "--instruction",
        action="append",
        dest="instructions",
        help="behavior instruction; repeat this option for multiple instructions",
    )
    parser.add_argument("--example-input", help="example user input")
    parser.add_argument("--example-output", help="example skill output")
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=REPO_ROOT / "skills",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config()
    try:
        behavior = prompt_value(args.behavior, "Behavior")
        if args.language_neutral:
            locale = None
        else:
            locale_input = prompt_value(
                args.locale,
                "Locale (or 'neutral')",
                str(config["default_locale"]),
            )
            locale = None if locale_input.lower() in {"neutral", "none"} else locale_input
        title = prompt_value(args.title, "Title", slugify(behavior).replace("-", " ").title())
        family_dir = args.skills_dir / slugify(behavior)
        family_description_en = None
        family_description_ko = None
        if not family_dir.exists():
            family_description_en = prompt_value(
                args.family_description_en, "Family description (English)"
            )
            family_description_ko = prompt_value(
                args.family_description_ko, "Family description (Korean)"
            )
        description = prompt_value(args.description, "Description")
        instructions = collect_instructions(args.instructions)
        example_input = prompt_value(args.example_input, "Example input")
        example_output = prompt_value(args.example_output, "Example output")
        output = create_skill(
            behavior=behavior,
            locale=locale,
            title=title,
            family_description_en=family_description_en,
            family_description_ko=family_description_ko,
            description=description,
            instructions=instructions,
            example_input=example_input,
            example_output=example_output,
            skills_dir=args.skills_dir,
        )
    except (ValueError, FileExistsError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Created {output.relative_to(REPO_ROOT) if output.is_relative_to(REPO_ROOT) else output}")
    print("Next: review the instructions, update both top-level README catalogs, and run `make check`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
