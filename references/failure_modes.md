# Failure modes

1. **Whole-token cross treated as deletion**
   - Fix: test state narration.

2. **Missing 5 treated as an index**
   - Fix: detect regular sequence and infer absence.

3. **Phrase rebus forced into one word**
   - Fix: allow a spoken sentence, then resegment.

4. **Orthography over phonetics**
   - Fix: in META_PHRASE_PUN compare sound stream.

5. **Arbitrary phonetic drift**
   - Fix: require close sound + coherent sentence + full visual accounting.

6. **Autocorrecting the result**
   - Fix: backtrack to the visual cue instead.

7. **Crossed letter confused with crossed card**
   - Fix: classify crossing scope explicitly.
