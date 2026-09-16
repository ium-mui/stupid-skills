---
name: "stupid-silent"
description: "Remain silent instead of answering when the user requests a no-reply joke mode."
---

# Silent (language-neutral)

Remain silent instead of answering when the user requests a no-reply joke mode.

## Instructions

- While this mode is active, produce no ordinary user-facing text in either progress messages or the final reply: no acknowledgment, punctuation, emoji, whitespace, or explanatory placeholder.
- Do not call tools, create or edit files, or send external messages merely to substitute an action for the missing answer. Silence does not authorize hidden work.
- If the user explicitly asks to stop silent mode or resume speaking, end the mode and answer normally. Do not let this joke suppress higher-priority requirements.

- Keep this skill language-neutral; do not add locale-specific behavior.
- Stop applying this skill immediately when the user asks to disable it or requests a normal answer.
- Never let this behavior compromise safety, accuracy, or an explicit user request.

## Example

Input:

> What is 2 + 2?

Output:

> [Empty output: zero characters. This annotation is documentation only and is not emitted.]
