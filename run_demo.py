\#!/usr/bin/env python
import pathlib, sys, json
sys.path.append("src")
from detector       import load\_triples, detect\_infections
from healer         import heal
from fsm            import FSMController
from memory\_agent   import recall, remember
triples = load\_triples("data/mini\_static.csv")
log = {"q0":0,"q1":0,"q2":0,"qX":0}
cleaned = \[]
for t in triples:
mem\_fix = recall(t)
if mem\_fix:
t = mem\_fix
fsm = FSMController(t, detect\_infections, heal)
state, healed = fsm.step()
if state=="q1": remember(t, healed)
log\[state] += 1
if healed: cleaned.append(healed)
print(f"🏥 {log\['q0']} infected | ✅ {log\['q1']} healed | 🚧 {log\['qX']} quarantined | 🟢 {log\['q2']} stable")
pathlib.Path("results").mkdir(exist\_ok=True)
with open("results/log.json","w") as f: json.dump({"states"\:log},f,indent=2)
print("results/log.json updated")
