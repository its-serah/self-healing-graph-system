from tinydb import TinyDB, Query
import hashlib, datetime, pathlib

DB_PATH = pathlib.Path("results/memory.json")
DB_PATH.parent.mkdir(exist_ok=True)
MEM = TinyDB(DB_PATH)

def _key(triple):
    return hashlib.md5(f"{triple['s']}{triple['p']}{triple['o']}".encode()).hexdigest()

def remember(triple, fix):
    MEM.insert({"key": _key(triple), "fix": fix,
                "timestamp": datetime.datetime.utcnow().isoformat()})

def recall(triple):
    hit = MEM.search(Query().key == _key(triple))
    return hit[0]["fix"] if hit else None
