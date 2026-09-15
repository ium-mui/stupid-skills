# stupid-skills

[한국어](README.ko.md)

A searchable collection of useless, unserious, and delightfully stupid AI skills.

Every installable skill starts with `stupid-` and belongs to a documented behavior family under `skills/<behavior>/`. Locale-specific behaviors are separate skills; language-neutral behaviors use a skill without a locale suffix. English is the canonical documentation language, and Korean translations are maintained alongside the English documents.

## Available skills

<!-- skills:start -->
| Skill | Locale | Behavior | Description | Install |
| --- | --- | --- | --- | --- |
| [`stupid-kkwettu-en-us`](skills/kkwettu/stupid-kkwettu-en-us) | `en-us` | `kkwettu` | Replace ordinary user-visible prose with 'kkwettu'. Use for the en-US variant of the stupid Kkwettu joke skill; never switch locale automatically. | `$skill-installer install https://github.com/ium-mui/stupid-skills/tree/main/skills/kkwettu/stupid-kkwettu-en-us` |
| [`stupid-kkwettu-ko`](skills/kkwettu/stupid-kkwettu-ko) | `ko` | `kkwettu` | Replace ordinary user-visible prose with '꿰뚜'. Use for the Korean variant of the stupid Kkwettu joke skill; never switch locale automatically. | `$skill-installer install https://github.com/ium-mui/stupid-skills/tree/main/skills/kkwettu/stupid-kkwettu-ko` |
| [`stupid-morse`](skills/morse/stupid-morse) | `neutral` | `morse` | Render ordinary conversational prose and prose file contents as International Morse code. Use when the user wants replies and written text transformed into Morse; preserve machine-readable syntax and exact literals. | `$skill-installer install https://github.com/ium-mui/stupid-skills/tree/main/skills/morse/stupid-morse` |
<!-- skills:end -->

## Install and use

From a Codex prompt, invoke the built-in skill installer with the GitHub URL of the exact skill directory. For the Korean Kkwettu variant:

```sh
$skill-installer install https://github.com/ium-mui/stupid-skills/tree/main/skills/kkwettu/stupid-kkwettu-ko
```

Use the install command in the catalog below for any other variant. The final URL segment must be the installable `stupid-*` directory, not its behavior-family parent. The installer refuses to overwrite an existing skill. The installed skill becomes available on the next turn; invoke it by name, for example `$stupid-kkwettu-ko`.

Install one locale variant of the same behavior at a time. A variant never detects or switches locale automatically.

`make` is not required to install a skill. It is the contributor harness used after cloning this repository to generate, synchronize, and validate submissions.

## Add a new skill

Run the interactive generator:

```sh
make new-skill
```

It asks for the behavior slug, locale or language-neutral mode, description, instructions, and an example. When creating a family for the first time, it also asks for English and Korean family descriptions. It then creates:

```text
skills/<behavior>/
├── README.md
├── README.ko.md
└── stupid-<behavior>[-<locale>]/
    └── SKILL.md
```

The generator automatically updates the variant list in both family READMEs and the top-level English/Korean catalogs. Review the generated files and run:

```sh
make check
```

The check validates every skill and runs the harness tests. Pull requests run the same check in GitHub Actions and require final code-owner approval from `@sibfuhsree` before merge.

## Supported locales

| Locale | Language | Default |
| --- | --- | --- |
| `en-us` | English (United States) | Yes |
| `ko` | Korean | No |

Supported locales and the `stupid` prefix are defined in [`config/repository.json`](config/repository.json).

A language-neutral skill has no locale suffix, such as `stupid-shrug`, but it still lives inside `skills/shrug/` with both family README files.

## Repository structure

```text
stupid-skills/
├── skills/
│   └── kkwettu/             Behavior family; not directly installable
│       ├── README.md         English family description
│       ├── README.ko.md      Korean family description
│       ├── stupid-kkwettu-en-us/
│       │   └── SKILL.md     Installable English variant
│       └── stupid-kkwettu-ko/
│           └── SKILL.md     Installable Korean variant
├── scripts/                 Generator and validation harness
├── templates/               New-skill template
├── tests/                   Harness tests
├── config/repository.json   Prefix and locale configuration
├── AGENTS.md                Repository rules for coding agents
├── CONTRIBUTING.md          Contribution guide
└── README.ko.md             Korean README translation
```

## Documentation

- [Contribution guide](CONTRIBUTING.md) · [한국어](CONTRIBUTING.ko.md)
- [Agent rules](AGENTS.md)

## Safety note

These skills are for jokes and experiments. Do not use them for important decisions, production work, or tasks that require accurate communication. A silly skill never overrides safety, correctness, or an explicit user request.

## License

MIT
