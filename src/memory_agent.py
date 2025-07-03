from tinydb import TinyDB, Query
import hashlib, datetime, pathlib
DB_PATH = pathlib.Path("results/memory.json")
DB_PATH.parent.mkdir(exist_ok=True)
MEM = TinyDB(DB_PATH)
def _key(t):
    return hashlib.md5(f"{t['s']}{t['p']}{t['o']}".encode()).hexdigest()
def remember(t, fix):
    MEM.insert({"key": _key(t), "fix": fix, "timestamp": datetime.datetime.utcnow().isoformat()})
def recall(t):
    hit = MEM.search(Query().key == _key(t))
    return hit[0]["fix"] if hit else None
