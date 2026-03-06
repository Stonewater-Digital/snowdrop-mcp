import json
from pathlib import Path

def atomic_write_json(path: Path, data: dict) -> None:
    """Write JSON state file atomically (write-to-temp, then rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    tmp.rename(path)
