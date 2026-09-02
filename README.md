# stupid-skills

[한국어](README.ko.md)

A searchable collection of useless, unserious, and delightfully stupid AI skills.

Every installable skill starts with `stupid-`, and every locale-specific behavior is a separate skill. English is the canonical documentation language; Korean translations are maintained alongside the English documents.

## Available skills

| Skill | Locale | Behavior |
| --- | --- | --- |
| [`stupid-kkwettu-en-us`](skills/stupid-kkwettu-en-us) | English (US) | Replaces ordinary prose with `kkwettu` |
| [`stupid-kkwettu-ko`](skills/stupid-kkwettu-ko) | Korean | Replaces ordinary prose with `꿰뚜` |

## Install and use

Clone the repository and copy the skill variant you want into your Codex skills directory.

```sh
git clone https://github.com/ium-mui/stupid-skills.git
cd stupid-skills
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/stupid-kkwettu-en-us "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart or reload Codex if needed, then invoke the installed skill by name, for example `$stupid-kkwettu-en-us`.

Install one locale variant of the same behavior at a time. A variant never detects or switches locale automatically.

## Add a new skill

Run the interactive generator:

```sh
make new-skill
```

It asks for the behavior slug, locale, description, instructions, and an example. It then creates:

```text
skills/stupid-<behavior>-<locale>/SKILL.md
```

Review the generated file, add the skill to both README catalogs, and run:

```sh
make check
```

The check validates every skill and runs the harness tests. Pull requests and pushes to `main` run the same check in GitHub Actions.

## Supported locales

| Locale | Language | Default |
| --- | --- | --- |
| `en-us` | English (United States) | Yes |
| `ko` | Korean | No |

Supported locales and the `stupid` prefix are defined in [`config/repository.json`](config/repository.json).

## Repository structure

```text
stupid-skills/
├── skills/                  Installable locale-specific skills
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
- [Agent rules](AGENTS.md) · [한국어](AGENTS.ko.md)

## Safety note

These skills are for jokes and experiments. Do not use them for important decisions, production work, or tasks that require accurate communication. A silly skill never overrides safety, correctness, or an explicit user request.

## License

MIT
