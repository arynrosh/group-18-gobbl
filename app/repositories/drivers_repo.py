from pathlib import Path
import json, os
from typing import List, Dict, Any

PATH = Path(__file__).resolve().parents[1] / "data" / "drivers.json"

def load_all_drivers() -> List[Dict[str, Any]]:
    if not PATH.exists():
        return []
    
    with PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_all_drivers(drivers: List[Dict[str, Any]]) -> None:
    tmp = PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(drivers, f, ensure_ascii=False, indent=2)

    os.replace(tmp, PATH)

""" def get_next_driver_id(drivers: List[Dict[str, Any]]) -> int:
    if not drivers:
        return 1
    return max(driver["id"] for driver in drivers ) + 1 """