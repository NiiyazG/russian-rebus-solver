#!/usr/bin/env python3
# Single-page verifier retained from v2. No bulk crawling.
import sys, json
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.alts=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="img":
            d=dict(attrs)
            if d.get("alt"): self.alts.append(d["alt"])

def main():
    if len(sys.argv)!=2:
        print("Usage: planetarebusov_probe.py <URL>"); return 2
    url=sys.argv[1]
    host=(urlparse(url).hostname or "").lower()
    if host not in {"planetarebusov.com","www.planetarebusov.com"}:
        raise SystemExit("Only planetarebusov.com URLs are accepted.")
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 HermesRebusSkill/2.1"})
    with urlopen(req,timeout=20) as r:
        html=r.read().decode("utf-8","replace")
    p=P(); p.feed(html)
    print(json.dumps({"url":url,"image_alt_count":len(p.alts),"alts":p.alts[:100]},ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
