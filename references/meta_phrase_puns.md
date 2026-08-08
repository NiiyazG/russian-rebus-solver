# META_PHRASE_PUN — state narration + phonetic resegmentation

## What this mode solves

Some rebuses do not encode a word through direct deletion/replacement. Instead, the picture describes the **state of a visible token**:

- token crossed out → it *was* there / it is no longer there;
- token left intact → it *is* there;
- expected sequence member missing → it *is not there*;
- repeated token → there are two/many of it.

The solver must first say this aloud, then re-segment the resulting sounds into normal Russian words.

This is a **metalinguistic phrase rebus**.

## Trigger detector

Raise `META_PHRASE_PUN` to high priority when at least 2 of these are true:

1. A red X crosses the **entire token/card**, not a single letter.
2. Two or more tokens use the same whole-token state marking.
3. Another token is visually intact/present, creating a present-vs-absent contrast.
4. A regular sequence deliberately skips exactly one item.
5. There are no normal answer boxes and the composition looks like a sentence/joke.
6. Standard deletion would erase large meaningful chunks and yield nonsense.
7. Reading the states as `был/была/есть/нет` produces plausible syllables.

## State narration grammar

### Crossed whole token X

Generate:
- `X был`
- `X была`
- `X было`
- `X были`
- optionally `X нет`, but lower priority when a contrasting present token suggests past-vs-present wording.

Important: grammatical agreement with X is not required in a sound rebus. The auxiliary may be selected because the **spoken fusion** creates the intended word.

Examples:
- `КО` crossed → `КО была` → `КОБЫЛА`
- `ЗА` crossed → `ЗА была` → `ЗАБЫЛА`

Do not "correct" `КО была` as normal prose. It is an intermediate sound construction.

### Present/intact token X

Generate:
- `X есть`
- `есть X`

High-priority fusion:
- `ПО есть` → `ПОЕСТЬ`

### Missing member N from a regular sequence

First infer the intended full sequence.

For `1 2 3 4 6 7 8 9`:
- expected: 1..9
- missing: 5

Then narrate absence:
- `пять нет`
- `пяти нет`
- `пяти нету`
- `пяти-то нет`
- `а пяти-то нету`

Under negation, the genitive form is often most natural:
`нет пяти`.

The particle `-то` may be required by the pun.

## Phonetic resegmentation

Word boundaries are soft.

Compare the **sound stream**, not only letters:

`А ПЯТИ-ТО` → approximately the same sound pattern as `АППЕТИТА`.

The helper engine uses a deliberately coarse Russian phonetic key:
- strips spaces/punctuation;
- Ё→Е;
- removes Ь/Ъ for coarse comparison;
- collapses doubled consonants;
- groups unstressed-like vowel classes.

This is a heuristic, not a pronunciation dictionary. Use it only as supporting evidence.

## Canonical image case

Visual inventory:
- card 1: `КО`, whole card/token crossed with a red X;
- card 2: `ЗА`, whole card/token crossed with a red X;
- card 3: `ПО`, intact and green;
- lower row: `1 2 3 4 6 7 8 9`; `5` absent.

Correct reasoning:

1. Whole-token crossing is a **state cue**, not character deletion.
2. `КО` was there → choose `КО была` → `КОБЫЛА`.
3. `ЗА` was there → `ЗА была` → `ЗАБЫЛА`.
4. `ПО` is there → `ПО есть` → `ПОЕСТЬ`.
5. Sequence lacks 5 → `а пяти-то нету`.
6. `а пяти-то` phonetically re-segments as `аппетита`.
7. Final phrase:
   **«Кобыла забыла поесть — аппетита нету».**

## Anti-error rules

- A whole-token X is not the same as a crossed letter inside a word.
- A missing sequence item is not automatically an index instruction.
- Do not insist on orthographic identity when the mode is explicitly phonetic/pun-based.
- Do not allow arbitrary phonetic drift. The resegmented phrase must still be close in sound and semantically coherent.
- Always show the literal narration before the final phrase so the user can verify the pun.
