# Ranking and backtracking

## Hard constraints

Reject or heavily penalize:
- unexplained strong visual marks;
- disappearing literal letters with no operator;
- ignored whole-token state contrast;
- ignored missing member of an obvious sequence;
- impossible indices;
- wrong answer length when boxes are clear.

## Standard score priorities

1. visual/operator accounting — 40%
2. length/box fit — 20%
3. natural Russian output — 18%
4. directness of picture labels — 8%
5. source/theme fit — 7%
6. source-specific convention fit — 5%
7. simplicity — 2%

## Meta-phrase adjustment

For `META_PHRASE_PUN`, replace "orthographic exactness" with:
- literal-state narration validity;
- phonetic closeness after resegmentation;
- sentence coherence.

A cross-word-boundary pun may be correct even if spellings differ.

Example:
`а пяти-то` and `аппетита` have a very close coarse phonetic key.

## Backtracking

If output is almost a word, never silently autocorrect.
Revisit:
- picture synonym;
- comma ownership;
- whole-token crossing vs local deletion;
- missing-sequence interpretation;
- auxiliary choice `был/была/было/были`;
- present `есть`;
- absence `нет/нету`;
- particle `-то`;
- phonetic resegmentation.
