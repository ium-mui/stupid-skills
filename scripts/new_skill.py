#!/usr/bin/env python3
"""Create one locale-specific stupid skill from the repository template."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "repository.json"
TEMPLATE_PATH = REPO_ROOT / "templates" / "SKILL.md.template"


def load_config(path: Path = CONFIG_PATH) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def one_line(value: str) -> str:
    return " ".join(value.split())


def blockquote(value: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in value.splitlines())


def create_skill(
    *,
    behavior: str,
    locale: str,
    description: str,
    instructions: list[str],
    example_input: str,
    example_output: str,
    title: str | None = None,
    skills_dir: Path | None = None,
    config_path: Path = CONFIG_PATH,
    template_path: Path = TEMPLATE_PATH,
) -> Path:
    config = load_config(config_path)
    prefix = str(config["skill_prefix"])
    supported_locales = {str(item) for item in config["supported_locales"]}

    behavior_slug = slugify(behavior)
    locale_slug = locale.strip().lower()
    if not behavior_slug:
        raise ValueError("behavior must contain at least one ASCII letter or digit")
    if locale_slug not in supported_locales:
        choices = ", ".join(sorted(supported_locales))
        raise ValueError(f"unsupported locale '{locale_slug}'; choose one of: {choices}")
    if not one_line(description):
        raise ValueError("description must not be empty")
    cleaned_instructions = [one_line(item) for item in instructions if one_line(item)]
    if not cleaned_instructions:
        raise ValueError("at least one instruction is required")
    if not example_input.strip() or not example_output.strip():
        raise ValueError("example input and output must not be empty")

    skill_name = f"{prefix}-{behavior_slug}-{locale_slug}"
    if len(skill_name) > 63:
        raise ValueError("generated skill name must be shorter than 64 characters")

    target_root = skills_dir or REPO_ROOT / "skills"
    target = target_root / skill_name
    if target.exists():
        raise FileExistsError(f"skill already exists: {target}")

    display_title = one_line(title) if title else behavior_slug.replace("-", " ").title()
    instruction_markdown = "\n".join(f"- {item}" for item in cleaned_instructions)
    description_text = one_line(description)
    replacements = {
        "{{SKILL_NAME_YAML}}": json.dumps(skill_name, ensure_ascii=False),
        "{{DESCRIPTION_YAML}}": json.dumps(description_text, ensure_ascii=False),
        "{{TITLE}}": display_title,
        "{{LOCALE}}": locale_slug,
        "{{DESCRIPTION_TEXT}}": description_text,
        "{{INSTRUCTIONS}}": instruction_markdown + "\n",
        "{{EXAMPLE_INPUT}}": blockquote(example_input.strip()),
        "{{EXAMPLE_OUTPUT}}": blockquote(example_output.strip()),
    }

    rendered = template_path.read_text(encoding="utf-8")
    for marker, value in replacements.items():
        rendered = rendered.replace(marker, value)
    if "{{" in rendered or "}}" in rendered:
        raise RuntimeError("the skill template contains an unresolved marker")

    target.mkdir(parents=True)
    output = target / "SKILL.md"
    output.write_text(rendered, encoding="utf-8")
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
    parser.add_argument("--locale", help="supported locale, such as en-us or ko")
    parser.add_argument("--title", help="human-readable skill title")
    parser.add_argument("--description", help="one-line discovery description")
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
        locale = prompt_value(args.locale, "Locale", str(config["default_locale"]))
        title = prompt_value(args.title, "Title", slugify(behavior).replace("-", " ").title())
        description = prompt_value(args.description, "Description")
        instructions = collect_instructions(args.instructions)
        example_input = prompt_value(args.example_input, "Example input")
        example_output = prompt_value(args.example_output, "Example output")
        output = create_skill(
            behavior=behavior,
            locale=locale,
            title=title,
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
    print("Next: review the instructions, update both README catalogs, and run `make check`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
