#!/usr/bin/env python3
import json, sys, re
from difflib import SequenceMatcher

NUMBER_WORDS = {
    0:"ноль",1:"один",2:"два",3:"три",4:"четыре",5:"пять",
    6:"шесть",7:"семь",8:"восемь",9:"девять",10:"десять",
    40:"сорок",100:"сто"
}
NUMBER_GENITIVE = {
    1:"одного",2:"двух",3:"трёх",4:"четырёх",5:"пяти",
    6:"шести",7:"семи",8:"восьми",9:"девяти",10:"десяти"
}

def transform(base, ops):
    s = str(base)
    trace = [s]
    for op in ops:
        kind = op["op"]
        if kind == "drop_left":
            s = s[int(op.get("n",1)):]
        elif kind == "drop_right":
            n=int(op.get("n",1)); s=s[:-n] if n else s
        elif kind == "reverse":
            s=s[::-1]
        elif kind == "replace":
            count=op.get("count",1)
            s=s.replace(str(op["old"]),str(op["new"])) if count=="all" else s.replace(str(op["old"]),str(op["new"]),int(count))
        elif kind == "delete_char":
            s=s.replace(str(op["char"]),"",int(op.get("count",1)))
        elif kind == "delete_index":
            i=int(op["index"])
            if not 1<=i<=len(s): raise ValueError("delete_index out of range")
            s=s[:i-1]+s[i:]
        elif kind == "indices":
            pos=[int(x) for x in op["positions"]]
            if any(i<1 or i>len(s) for i in pos): raise ValueError("indices out of range")
            s="".join(s[i-1] for i in pos)
        elif kind == "swap":
            i,j=int(op["i"]),int(op["j"])
            chars=list(s); chars[i-1],chars[j-1]=chars[j-1],chars[i-1]; s="".join(chars)
        elif kind == "prefix":
            s=str(op.get("text",""))+s
        elif kind == "suffix":
            s=s+str(op.get("text",""))
        else:
            raise ValueError(f"unknown op {kind}")
        trace.append(s)
    return {"result":s,"trace":trace}

def detect_missing_sequence(values):
    nums=sorted({int(x) for x in values})
    if len(nums)<2: return []
    expected=set(range(nums[0],nums[-1]+1))
    return sorted(expected-set(nums))

def state_variants(token, state, value=None):
    token=str(token)
    if state=="crossed_whole":
        return [f"{token} была",f"{token} был",f"{token} было",f"{token} были",f"{token} нет"]
    if state=="present":
        return [f"{token} есть",f"есть {token}"]
    if state=="missing_number":
        n=int(value if value is not None else token)
        nom=NUMBER_WORDS.get(n,str(n))
        gen=NUMBER_GENITIVE.get(n,nom)
        return [
            f"{nom} нет",
            f"{gen} нет",
            f"{gen} нету",
            f"{gen}-то нет",
            f"а {gen}-то нету",
        ]
    if state=="missing":
        return [f"{token} нет",f"{token}-то нет",f"а {token}-то нету"]
    if state=="repeated":
        return [f"два {token}",f"{token} дважды",f"много {token}"]
    return [token]

def phonetic_key_ru(s):
    s=str(s).lower().replace("ё","е")
    s=re.sub(r"[^а-я]+","",s)
    s=s.replace("ь","").replace("ъ","")
    out=[]
    last=None
    for ch in s:
        if ch in "ао":
            ch="а"
        elif ch in "еияыэ":
            ch="и"
        elif ch in "ую":
            ch="у"
        if ch==last and ch not in "аиу":
            continue
        out.append(ch)
        last=ch
    return "".join(out)

def phonetic_compare(a,b):
    ka,kb=phonetic_key_ru(a),phonetic_key_ru(b)
    return {
        "a_key":ka,
        "b_key":kb,
        "similarity":round(SequenceMatcher(None,ka,kb).ratio(),4),
        "match":ka==kb
    }

def main():
    if len(sys.argv)<3:
        print("Usage: rebus_engine.py transform|missing|state|phonetic '<json>'")
        return 2
    cmd=sys.argv[1]; data=json.loads(sys.argv[2])
    if cmd=="transform":
        out=transform(data.get("base",""),data.get("ops",[]))
    elif cmd=="missing":
        out={"missing":detect_missing_sequence(data["values"])}
    elif cmd=="state":
        out={"variants":state_variants(data.get("token",""),data["state"],data.get("value"))}
    elif cmd=="phonetic":
        out=phonetic_compare(data["a"],data["b"])
    else:
        raise SystemExit("unknown command")
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
