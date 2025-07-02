#!/usr/bin/env python
import json, datetime, pathlib, sys
sys.path.append("src")
from detector import load_triples, detect_infections
from healer   import heal

triples   = load_triples("data/mini_static.csv")
infected  = detect_infections(triples)
log, clean = [], []

for row in triples:
    tags   = [t for (tr, t) in infected if tr is row]
    healed = row
    for tag in tags:
        healed = heal(dict(healed), tag) if healed else None
    state  = "q0" if tags else "q2"
    if healed and tags: state = "q1"
    if not healed:      state = "qX"
    if healed: clean.append(healed)
    log.append({"triple": row, "tags": tags, "state": state})

print(f"🏥 {len(infected)} infected | ✅ {len([l for l in log if l['state']=='q1'])} healed | 🚧 {len([l for l in log if l['state']=='qX'])} quarantined")
pathlib.Path('results').mkdir(exist_ok=True)
with open('results/log.json','w') as f: json.dump(log,f,indent=2)
print('results/log.json written')
