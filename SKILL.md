---
name: russian-rebus-solver
description: High-coverage Russian visual rebus solver for Hermes Agent. Solves and explains Russian rebuses from images, screenshots, scans, PDFs, webpages, or text descriptions. Classifies the puzzle before decoding among 10+ modes: STANDARD (pictures + letters + commas + replacement + indices), SPATIAL (in/at/on/behind/from/by/along/with), PLANET_DIALECT (planetarebusov.com conventions), META_PHRASE_PUN (whole tokens present/crossed/missing narrated as "was/is/not" then phonetically re-segmented into a phrase), LOGOPEDIC (sounds), MUSICAL (notes ДО/РЕ/МИ/ФА/СОЛЬ/ЛЯ/СИ), THEMATIC, LITERARY (names/titles/characters), CHESS, BILINGUAL. Uses explicit visual accounting (perception protocol: letters, digits, comma count, crossed letter vs crossed whole token, arrows, pointing hands, rotation, answer boxes, missing members of regular sequences, status contrast crossed/intact/absent/repeated/highlighted), multi-hypothesis picture naming with synonyms, deterministic operators (commas, deletion, replacement А=Б, indices, permutation, reversal, literal affixes, number readings, notes), spatial grammar with prepositions (И,К,ЗА,В,НА,НЕ,ОТ,У,ПО,С) and pointing finger as К, meta phrase/pun grammar with spoken narration ("был/была/есть/нет/нету/-то") and phonetic re-segmentation across word boundaries (e.g. КО×+ЗА×+ПО+missing 5 → "Кобыла забыла поесть — аппетита нету"), hypothesis branching and backtracking ladder, ranking by visual accounting, fit, naturalness, source consistency and minimal assumptions. Includes helper scripts (rebus_engine.py transform/phonetic, planetarebusov_probe.py) and self-tests. Prefers rigorous decoding over guessing and never claims 100% accuracy without a full benchmark.
version: 2.1.0
author: Custom skill
license: MIT
platforms: [macos, linux, windows]
---

# Russian Rebus Solver v2.1

Use this skill whenever the user asks to solve, explain, verify, or analyze a Russian rebus from an image, screenshot, scan, PDF, webpage, or text description.

The solver must prefer **explicit visual accounting + multiple hypotheses + backtracking** over guessing.

## 0. Classify the rebus BEFORE applying operators

Keep one or more modes alive until evidence rules them out:

- `STANDARD` — pictures + letters + commas + replacement + indices.
- `SPATIAL` — elements arranged in/at/on/behind/from/by/along/with each other.
- `PLANET_DIALECT` — source-specific conventions used by planetarebusov.com.
- `META_PHRASE_PUN` — whole tokens are present/crossed/missing and must first be narrated as "был/была/есть/нет", then phonetically re-segmented into a phrase.
- `LOGOPEDIC` — pictures encode sounds.
- `MUSICAL` — notes encode ДО/РЕ/МИ/ФА/СОЛЬ/ЛЯ/СИ or music vocabulary.
- `THEMATIC` — winter, transport, animals, vegetables/fruit, etc.
- `LITERARY` — answer is likely a name/title/character.
- `CHESS` — chess vocabulary/figures/moves.
- `BILINGUAL` — only when the source explicitly targets another language.

### Critical precedence rule

Do **not** automatically interpret every red cross as "delete these letters".

If an **entire syllable/token/card** is crossed, especially when:
- other whole tokens are also crossed;
- another token is explicitly present/intact;
- a regular numeric/alphabetic sequence has one missing member;
- the result likely forms a sentence or joke;

then test `META_PHRASE_PUN` **before** standard deletion.

Load:
`${HERMES_SKILL_DIR}/references/meta_phrase_puns.md`

## 1. Literal visual inventory

Load:
`${HERMES_SKILL_DIR}/references/perception_protocol.md`

Record:
- every picture;
- every visible syllable/letter;
- every digit;
- commas and exact count/side;
- equality signs and replacements;
- crossed **letter** vs crossed **whole token**;
- arrows and direction;
- pointing hands/fingers;
- rotation/reversal;
- answer boxes if any;
- relative geometry;
- regular sequences and missing members;
- status contrast: crossed / intact / absent / repeated / highlighted.

Do not use OCR alone. Geometry and state are semantic.

## 2. Decide whether the puzzle encodes a word or a spoken phrase

Strong signals of a **phrase-level/meta rebus**:
- 3+ independent blocks;
- whole blocks carry states (crossed/intact/absent);
- a sequence has a deliberately missing element;
- direct character deletion makes no sensible word;
- visual states can be narrated naturally with `был/была/было/были`, `есть`, `нет/нету`;
- these narrations become Russian words after removing/reassigning word boundaries.

If these signals are present, build a **literal narration first**, then perform phonetic resegmentation.

## 3. Picture-name hypotheses

For each picture, generate at least 3 plausible Russian names unless unambiguous:
1. direct noun;
2. common synonym;
3. short/long, generic/specific, singular/plural variant.

For difficult images use 5–10 candidates.

If source hints exist, use them as picture-name priors, not as final answers.

## 4. Apply deterministic local operators

Load:
`${HERMES_SKILL_DIR}/references/operators.md`

Use commas, deletion, replacement, indices, permutations, reversal, literal prefixes/suffixes, notes, number readings, etc.

Helper:

```bash
python "${HERMES_SKILL_DIR}/scripts/rebus_engine.py" transform '{"base":"ЛИПА","ops":[{"op":"indices","positions":[3,2,1,4]}]}'
```

## 5. Spatial grammar

Load:
`${HERMES_SKILL_DIR}/references/spatial_grammar.md`

For Planet Rebus Book 3 explicitly test:
`И, К, ЗА, В, НА, НЕ, ОТ, У, ПО, С`.

A pointing finger can be the relation `К`, not the noun "палец/рука".

## 6. Meta phrase/pun grammar

When `META_PHRASE_PUN` is active:

1. Classify each token state:
   - `crossed_whole`
   - `present`
   - `missing_from_sequence`
   - `repeated`
   - `highlighted`
2. Convert the state into **spoken narration variants**:
   - crossed whole X → `X был / X была / X было / X были / X нет`
   - present X → `X есть / есть X`
   - missing N → `N нет / N-то нет / а N-то нету`
3. If a number is missing, use the grammatically natural form under negation:
   - 5 → `пяти`
   - so `а пяти-то нету` is a valid narration candidate.
4. Concatenate the narration **as speech**, not merely as spelling.
5. Re-segment sounds across word boundaries into ordinary Russian words.
6. Rank by:
   - phonetic closeness;
   - coherent sentence meaning;
   - use of every visual state;
   - minimal arbitrary edits.

Helper:

```bash
python "${HERMES_SKILL_DIR}/scripts/rebus_engine.py" phonetic '{"a":"а пяти-то","b":"аппетита"}'
```

### Canonical regression case

Visual:
- `КО` crossed as a whole;
- `ЗА` crossed as a whole;
- `ПО` intact/present;
- sequence `1 2 3 4 6 7 8 9` with `5` missing.

Literal narration:
- `КО была`
- `ЗА была`
- `ПО есть`
- `а ПЯТИ-то нету`

Phonetic resegmentation:
- `КО БЫЛА` → `КОБЫЛА`
- `ЗА БЫЛА` → `ЗАБЫЛА`
- `ПО ЕСТЬ` → `ПОЕСТЬ`
- `А ПЯТИ-ТО` ≈ `АППЕТИТА`

Answer:
**«Кобыла забыла поесть — аппетита нету».**

This case must **not** be solved by deleting `КО` and `ЗА`.

## 7. Search hypotheses instead of guessing

For ambiguity:
- branch picture names;
- branch comma attachment;
- branch arrow role;
- branch number mode;
- branch standard vs meta-state interpretation;
- keep the strongest 10–30 partial hypotheses.

Reject candidates that leave a strong visible cue unexplained.

## 8. Ranking

Load:
`${HERMES_SKILL_DIR}/references/ranking_and_backtracking.md`

Highest priority:
1. 100% visual-state/operator accounting;
2. exact length/box grouping when supplied;
3. phonetic or orthographic fit appropriate to the selected mode;
4. natural Russian word/phrase;
5. thematic/source consistency;
6. fewest assumptions.

## 9. Backtracking ladder

If the first solution fails:

1. Recount visible elements.
2. Distinguish crossed letter vs crossed whole token.
3. Check whether a regular sequence has an omitted member.
4. Reassign ambiguous commas.
5. Try picture synonyms.
6. Re-evaluate reversal vs spatial arrow.
7. Re-evaluate digits as indices vs spoken numbers.
8. Re-evaluate pointing hand as `К`.
9. Try `META_PHRASE_PUN` if multiple present/absent states occur.
10. In meta mode, try `был/была/было/были`, `есть`, `нет/нету`, `-то`.
11. Compare phonetic keys across word boundaries.
12. Switch logopedic/musical mode if source category supports it.
13. Only then use external source verification.

## 10. Response format

**Ответ:** <answer>

**Разбор:**
1. `<visual block>` → `<literal reading/state>`
2. ...
3. `<spoken narration>` → `<phonetic/orthographic resegmentation>`
4. Получаем: **<answer>**

**Почему не другой вариант:** briefly mention the rejected interpretation if the visual operator was ambiguous.

**Уверенность:** высокая / средняя / низкая.

## Quality rule

Do not claim 100% accuracy on all 10,000+ source puzzles unless a complete benchmark has actually been run. This skill is designed for full-category coverage, but image quality and author-specific conventions can still cause failures.
