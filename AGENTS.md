# Repository rules

[한국어](AGENTS.ko.md)

These rules apply to every automated agent and contributor working in this repository.

## Skills

- Treat each direct child of `skills/` as one independently installable skill.
- Name skills `stupid-<behavior>-<locale>` using lowercase ASCII letters, digits, and hyphens.
- Keep the folder name and the `name` in YAML frontmatter identical.
- Keep a required uppercase `SKILL.md` at the root of every skill folder.
- Use only locales declared in `config/repository.json`.
- Keep each locale variant fixed. Never add automatic locale detection or fallback to another variant.
- Do not add empty resource directories. Add `scripts/`, `references/`, `assets/`, or `agents/` only when the skill actually needs them.

## Documentation

- Write canonical repository documentation in English.
- Maintain a matching Korean `.ko.md` translation for public documentation.
- Update both README skill tables whenever a skill is added, renamed, or removed.
- Keep skill metadata and instructions concise and behavior-specific.

## Workflow

- Prefer `make new-skill` when creating a skill.
- Never overwrite an existing skill during generation.
- Run `make check` after changing skills, configuration, templates, scripts, or tests.
- Preserve unrelated user changes and do not weaken validation to make invalid content pass.
