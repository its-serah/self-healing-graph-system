import csv, yaml, hashlib
from pathlib import Path

CONFIG = yaml.safe_load(open("config/infection_rules.yaml"))
CUTOFF = CONFIG["confidence_cutoff"]
FUNC_PRED = set(CONFIG["functional_predicates"])
TYPE_MAP = CONFIG["type_map"]

def load_triples(path="data/mini_static.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def detect_infections(triples):
    # key = (s,p); store best triple for R2
    seen = {}
    infected = []

    for row in triples:
        s, p, o = row["s"], row["p"], row["o"]
        conf     = float(row.get("confidence", 1.0))

        # R1 — confidence drop
        if conf < CUTOFF:
            infected.append((row, "R1"))
            continue

        # R2 — functional clash
        key = (s, p)
        if p in FUNC_PRED:
            if key in seen and seen[key]["o"] != o:
                infected.append((row, "R2"))
                infected.append((seen[key], "R2"))
            else:
                seen[key] = row

        # R3 — schema violation
        expected = TYPE_MAP.get(p)
        if expected == "date" and len(o) != 10:
            infected.append((row, "R3"))

    return infected
