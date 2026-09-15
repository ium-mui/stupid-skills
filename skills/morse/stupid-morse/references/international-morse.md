# International Morse reference

Use uppercase Latin letters for lookup. Encode letters with one space between them, words with ` / `, and retain source line breaks.

## Letters

| Letter | Code | Letter | Code | Letter | Code | Letter | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | `.-` | B | `-...` | C | `-.-.` | D | `-..` |
| E | `.` | F | `..-.` | G | `--.` | H | `....` |
| I | `..` | J | `.---` | K | `-.-` | L | `.-..` |
| M | `--` | N | `-.` | O | `---` | P | `.--.` |
| Q | `--.-` | R | `.-.` | S | `...` | T | `-` |
| U | `..-` | V | `...-` | W | `.--` | X | `-..-` |
| Y | `-.--` | Z | `--..` | | | | |

## Digits

| Digit | Code | Digit | Code | Digit | Code | Digit | Code | Digit | Code |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `-----` | 1 | `.----` | 2 | `..---` | 3 | `...--` | 4 | `....-` |
| 5 | `.....` | 6 | `-....` | 7 | `--...` | 8 | `---..` | 9 | `----.` |

## Common punctuation

| Character | Code | Character | Code | Character | Code |
| --- | --- | --- | --- | --- | --- |
| `.` | `.-.-.-` | `,` | `--..--` | `?` | `..--..` |
| `'` | `.----.` | `!` | `-.-.--` | `/` | `-..-.` |
| `(` | `-.--.` | `)` | `-.--.-` | `&` | `.-...` |
| `:` | `---...` | `;` | `-.-.-.` | `=` | `-...-` |
| `+` | `.-.-.` | `-` | `-....-` | `_` | `..--.-` |
| `"` | `.-..-.` | `$` | `...-..-` | `@` | `.--.-.` |

## Conversion rules

- Transliterate non-Latin prose to plain Latin first, then encode the transliteration. Do not silently translate its meaning into another language.
- Preserve an unknown character literally only when no safe transliteration or Morse representation exists.
- In prose-only files, encode all headings, paragraphs, captions, list text, and labels.
- In code or structured files, preserve syntax, keys, identifiers, paths, URLs, and exact literals. Encode only human-facing prose where doing so does not invalidate the artifact.
- Keep fenced code, commands, and exact strings unencoded. Resume Morse immediately after the exact block.
- When an intelligible safety warning or error is necessary, state it normally; safety and correctness override the joke transformation.
