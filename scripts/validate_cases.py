#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/"scripts"))
from rebus_engine import transform, detect_missing_sequence, state_variants, phonetic_compare

failed=[]
cases=json.loads((ROOT/"tests"/"transform_cases.json").read_text(encoding="utf-8"))
for c in cases:
    got=transform(c["base"],c["ops"])["result"]
    if got!=c["expected"]:
        failed.append((c["name"],got,c["expected"]))

m=json.loads((ROOT/"tests"/"meta_phrase_case.json").read_text(encoding="utf-8"))
missing=detect_missing_sequence(m["visual_parse"]["sequence"])
if missing!=m["expected_missing"]:
    failed.append(("missing_sequence",missing,m["expected_missing"]))

# State variants must contain the intended literal narration.
for token, state, expected in [
    ("КО","crossed_whole","КО была"),
    ("ЗА","crossed_whole","ЗА была"),
    ("ПО","present","ПО есть"),
]:
    vals=state_variants(token,state)
    if expected not in vals:
        failed.append((f"state_{token}",vals,expected))

vals=state_variants("5","missing_number",5)
if "а пяти-то нету" not in vals:
    failed.append(("state_missing_5",vals,"а пяти-то нету"))

for a,b in m["resegmented"]:
    cmp=phonetic_compare(a,b)
    if not cmp["match"]:
        failed.append((f"phonetic:{a}->{b}",cmp,"exact coarse-key match"))

if failed:
    for x in failed: print("FAIL",x)
    raise SystemExit(1)

print(f"OK: {len(cases)} standard transform tests + missing-sequence + 4 state tests + {len(m['resegmented'])} phonetic resegmentation tests passed.")
