#!/usr/bin/env python3
import json

with open('results/log.json') as f:
    log = json.load(f)

print("\n=== Knowledge Graph Healing Results ===\n")
for entry in log:
    triple = entry['triple']
    state_map = {
        'q0': '🔄 Processing',
        'q1': '✅ Healed',
        'q2': '✨ Clean',
        'qX': '🚫 Quarantined'
    }
    status = state_map.get(entry['state'], entry['state'])
    tags = f" (Rules: {', '.join(entry['tags'])})" if entry['tags'] else ""
    
    print(f"{status}{tags}")
    print(f"  {triple['s']} --[{triple['p']}]--> {triple['o']}")
    if 'confidence' in triple:
        print(f"  Confidence: {triple['confidence']}")
    print()
