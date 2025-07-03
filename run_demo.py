#!/usr/bin/env python
import pathlib, sys, json
sys.path.append("src")

from detector       import load_triples, detect_infections
from healer         import heal
from fsm            import FSMController
from memory_agent   import recall, remember

triples  = load_triples("data/mini_static.csv")
log      = {"q0":0, "q1":0, "q2":0, "qX":0}
cleaned  = []

for t in triples:
    cached_fix = recall(t)
    if cached_fix: t = cached_fix

    fsm = FSMController(t, detect_infections, heal)
    state, healed = fsm.step()

    if state == "q1": remember(t, healed)   # store fix for future
    log[state] += 1
    if healed: cleaned.append(healed)

print(f"🏥 {log['q0']} infected | ✅ {log['q1']} healed | 🚧 {log['qX']} quarantined | 🟢 {log['q2']} stable")

pathlib.Path("results").mkdir(exist_ok=True)
with open("results/log.json", "w") as f:
    json.dump({"states": log}, f, indent=2)
print("📝  results/log.json updated")
