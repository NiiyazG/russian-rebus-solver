# Benchmark protocol

For full-corpus validation store per puzzle:
- source category/page;
- target answer;
- mode(s);
- visual parse;
- predicted answer;
- top-3;
- exact match;
- full-symbol accounting;
- failure type.

Add failure classes:
- `WHOLE_TOKEN_STATE`
- `MISSING_SEQUENCE`
- `META_PHRASE_ROUTING`
- `PHONETIC_RESEGMENTATION`
- `AUXILIARY_VARIANT`
- `PARTICLE_TO`

Do not claim 100% coverage until every available source item has been actually benchmarked.
