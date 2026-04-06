import json
import os
from pathlib import Path
from typing import List, Dict, Any

DIET_RESTRICTIONS_PATH = Path(__file__).resolve().parents[1] / "data" / "diet_restrictions.json"


def load_all_diet_restrictions() -> List[Dict[str, Any]]:
    if not DIET_RESTRICTIONS_PATH.exists():
        return []
    with DIET_RESTRICTIONS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_all_diet_restrictions(diet_restrictions: List[Dict[str, Any]]) -> None:
    tmp = DIET_RESTRICTIONS_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(diet_restrictions, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DIET_RESTRICTIONS_PATH)