# Contributing

[한국어](CONTRIBUTING.ko.md)

Contributions should keep stupid skills easy to discover, install, and understand.

## Naming rules

- Group variants under `skills/<behavior>/`.
- Use `stupid-<behavior>-<locale>` for localized behavior.
- Use `stupid-<behavior>` for language-neutral behavior.
- Use lowercase ASCII letters, digits, and single hyphens.
- Keep the name shorter than 64 characters.
- Make the folder name and frontmatter `name` identical.
- Use only locales listed in `config/repository.json`.

Examples:

```text
skills/kkwettu/stupid-kkwettu-en-us/SKILL.md
skills/kkwettu/stupid-kkwettu-ko/SKILL.md
skills/random-footnote/stupid-random-footnote-en-us/SKILL.md
skills/shrug/stupid-shrug/SKILL.md
```

Every family must contain an English `README.md` and a Korean `README.ko.md` explaining the shared behavior and listing all variants. The family directory must not contain a `SKILL.md` or files other than those two READMEs. The nested `stupid-*` directory is the installable skill and must remain self-contained when copied out of its family.

## Locale rules

Each locale variant is an independent skill. It must always use its declared locale behavior, regardless of the input language, and must never switch locale automatically.

Use a language-neutral skill only when its behavior and output do not depend on language. It still requires a family and both translated family READMEs.

If two variants differ only by translated output, they are still separate installable skills. If they also differ in tone, formatting, or joke behavior, document those differences directly in each `SKILL.md`.

English is the default documentation language. When changing a public repository document, update its `.ko.md` translation in the same pull request.

## Create a skill

Run:

```sh
make new-skill
```

The generator creates both family READMEs when needed, updates their variant catalogs, and refuses unsupported locales, invalid names, and existing target directories. After generation:

1. Review the generated `SKILL.md` and make its behavior unambiguous.
2. Add a concise, discriminating frontmatter description.
3. Keep at least one realistic input/output example.
4. Update the skill tables in `README.md` and `README.ko.md`.
5. Run `make check`.

## Add a locale

Add its lowercase locale identifier to `supported_locales` in `config/repository.json`, update both READMEs and contribution guides, and add at least one real skill or harness test using that locale.

Use a language code such as `ko` when regional behavior does not matter. Use a regional code such as `en-us` when it does.

## Pull request checklist

- The skill has a unique `stupid-` name.
- Its family has synchronized English and Korean READMEs.
- The folder contains a required `SKILL.md`.
- A localized skill keeps its locale fixed and does not change automatically.
- English and Korean public documentation remain synchronized.
- `make check` passes.
