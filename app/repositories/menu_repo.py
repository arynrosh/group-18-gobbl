from pathlib import Path
import json, os
from typing import List, Dict, Any

PATH = Path(__file__).resolve().parents[1] / "data" / "menu.json"

def load_all_menu_items() -> List[Dict[str, Any]]:
    if not PATH.exists():
        return []
    
    with PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_all_menu_items(items: List[Dict[str, Any]]) -> None:
    tmp = PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    os.replace(tmp, PATH)

def get_next_menu_id(items: List[Dict[str, Any]]) -> int:
    if not items:
        return 1
    return max(item["menu_item_id"] for item in items ) + 1