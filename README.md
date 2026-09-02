# stupid-skills

A collection of useless, unserious, and delightfully stupid AI skills.

The goal of this repository is not to improve productivity. It is to give an AI deliberately meaningless behaviors and make the skill system fun to experiment with.

English is the default repository language and the default variant language. Each language variant is packaged as an independent skill so it can be installed and enabled on its own.

## Available skills

| Skill | Description | Default |
| --- | --- | --- |
| [`kkwettu-en-US`](skills/kkwettu-en-US) | Replaces ordinary prose with `kkwettu` | Yes |
| [`kkwettu-ko`](skills/kkwettu-ko) | Replaces ordinary prose with `꿰뚜` | No |

## Install a skill

Copy one skill directory into the Codex skills directory.

```sh
cp -R skills/kkwettu-en-US "$CODEX_HOME/skills/"
```

To use the Korean variant instead:

```sh
cp -R skills/kkwettu-ko "$CODEX_HOME/skills/"
```

Use one variant at a time. Combining multiple variants can produce conflicting instructions.

## Design principles

- Every installable variant has its own `SKILL.md`.
- Skill and directory names use stable ASCII slugs with a locale suffix.
- Documentation and metadata are written in English by default.
- Variants may have completely different nonsense behaviors, not just translated instructions.

## Safety note

These skills are for jokes and experiments. Do not use them for important decisions, production code, translation, or work that requires accurate communication. A silly skill never overrides safety, correctness, or the user's explicit request.

## Contributing

When adding a new stupid skill, include:

- A short and clear `SKILL.md`
- A funny example input and output
- A warning when the behavior could interfere with real work
- An explicit locale suffix when the behavior is language-specific

## License

MIT
