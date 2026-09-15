# Repository rules

These rules apply to every automated agent and contributor working in this repository.

## Skills

- Treat each direct child of `skills/` as a behavior family used only for repository navigation.
- Place each localized skill at `skills/<behavior>/stupid-<behavior>-<locale>/`.
- Place each language-neutral skill at `skills/<behavior>/stupid-<behavior>/`.
- Name skills using lowercase ASCII letters, digits, and hyphens.
- Keep the folder name and the `name` in YAML frontmatter identical.
- Encode frontmatter `name` and `description` as JSON-quoted strings so validation is deterministic without repository-specific YAML extensions.
- Keep a required uppercase `SKILL.md` at the root of every skill folder.
- Require `README.md` and `README.ko.md` in every behavior family, even when it contains one variant or one language-neutral skill.
- Do not place `SKILL.md` or files other than the two family READMEs directly in a behavior family folder.
- Use only locales declared in `config/repository.json`.
- Keep each locale variant fixed. Never add automatic locale detection or fallback to another variant.
- Do not add empty resource directories. Add `scripts/`, `references/`, `assets/`, or `agents/` only when the skill actually needs them.

## Documentation

- Write canonical repository documentation in English.
- Keep `AGENTS.md` English-only because it is an automation harness, not user-facing documentation.
- Maintain Korean translations in the top-level README, each behavior-family README, and other user-facing contribution documentation.
- Update both README skill tables whenever a skill is added, renamed, or removed.
- Keep each family README's generated variant catalog intact and synchronized.
- Keep skill metadata and instructions concise and behavior-specific.

## Workflow

- Document `$skill-installer install <GitHub skill-folder URL>` as the public installation path. Keep `make` and `scripts/` commands for contributors working in a clone.
- Prefer `make new-skill` when creating a skill.
- Never overwrite an existing skill during generation.
- Run `make check` after changing skills, configuration, templates, scripts, or tests.
- Preserve unrelated user changes and do not weaken validation to make invalid content pass.
