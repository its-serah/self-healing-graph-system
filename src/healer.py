def heal(triple, rule_tag):
    if rule_tag == "R2":
        # simply drop lower-confidence duplicate
        return None  # returning None = delete
    if rule_tag == "R3":
        # try to cast string '1990' → '1990-01-01'
        obj = triple["o"]
        if len(obj) == 4 and obj.isdigit():
            triple["o"] = f"{obj}-01-01"
            triple["confidence"] = 0.8
            return triple
    # R1 → quarantine, no auto-fix
    return triple
