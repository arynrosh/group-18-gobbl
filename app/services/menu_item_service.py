import json
from pathlib import Path
from typing import List
from app.schemas.menu_item import MenuItem

MENU_PATH = Path(__file__).resolve().parents[1] / "data" / "menu.json"

def _load_menu_items() -> List[dict]:
    """Loads all menu items from the JSON file."""
    if not MENU_PATH.exists():
        return []
    with MENU_PATH.open(encoding="utf-8") as f:
        return json.load(f)

def search_by_name(name: str) -> List[MenuItem]:
    """Searches menu items by name across all restaurants."""
    menu_items = _load_menu_items()
    return [
        MenuItem(**item)
        for item in menu_items
        if name.lower() in item["food_item"].lower()
    ]
