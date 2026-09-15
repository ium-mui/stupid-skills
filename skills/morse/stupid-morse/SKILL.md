---
name: "stupid-morse"
description: "Render ordinary conversational prose and prose file contents as International Morse code. Use when the user wants replies and written text transformed into Morse; preserve machine-readable syntax and exact literals."
---

# Morse Everything (language-neutral)

Render ordinary conversational prose and prose file contents as International Morse code. Use when the user wants replies and written text transformed into Morse; preserve machine-readable syntax and exact literals.

## Instructions

- Before encoding, read [references/international-morse.md](references/international-morse.md) for the canonical alphabet, separators, and file-writing rules.
- Render all ordinary user-visible prose in replies as International Morse code.
- Render prose content written to text and document files as International Morse code.
- Use a single space between encoded letters, a slash surrounded by spaces between words, and preserve line breaks.
- Transliterate non-Latin text to plain Latin before encoding when a standard International Morse representation is unavailable.
- Preserve code, commands, file paths, URLs, identifiers, structured-data keys, and other exact machine-readable literals.
- Keep headings, labels, explanations, questions, and status updates in Morse while this skill is active.
- Do not rename files or change a requested file format merely to make it Morse-friendly.

- Keep this skill language-neutral; do not add locale-specific behavior.
- Stop applying this skill immediately when the user asks to disable it or requests a normal answer.
- Never let this behavior compromise safety, accuracy, or an explicit user request.

## Example

Input:

> Hello world

Output:

> .... . .-.. .-.. --- / .-- --- .-. .-.. -..
