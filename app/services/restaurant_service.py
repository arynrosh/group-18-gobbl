import json
from pathlib import Path
from typing import List
from app.schemas.restaurant import Restaurant

MENU_PATH = Path(__file__).resolve().parents[1] / "data" / "menu.json"

def _load_restaurants() -> List[Restaurant]:
    """Loads unique restaurants from the menu JSON file."""
    if not MENU_PATH.exists():
        return []
    with MENU_PATH.open(encoding="utf-8") as f:
        menu_items = json.load(f)
    seen = set()
    restaurants = []
    for item in menu_items:
        if item["restaurant_id"] not in seen:
            seen.add(item["restaurant_id"])
            restaurants.append(Restaurant(
                restaurant_id=item["restaurant_id"],
                restaurant_name=item["restaurant_name"],
                cuisine=item["cuisine"]
            ))
    return restaurants

def search_by_name(name: str) -> List[Restaurant]:
    """Search restaurants by name."""
    return [r for r in _load_restaurants() if name.lower() in r.restaurant_name.lower()]

def search_by_cuisine(cuisine: str) -> List[Restaurant]:
    """Search restaurants by cuisine type."""
    return [r for r in _load_restaurants() if cuisine.lower() in r.cuisine.lower()]