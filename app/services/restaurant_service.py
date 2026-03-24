import csv
from pathlib import Path
from typing import List
from app.schemas.restaurant import Restaurant

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.csv"

def _load_restaurants() -> List[dict]:
    """Loads all restaurants from the CSV file."""
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            {
                "id": int(row["restaurant_id"]),
                "name": row["name"],
                "cuisine": row["cuisine"],
                "location": row["location"]
            }
            for row in reader
        ]

def _search_by_field(field: str, query: str) -> List[Restaurant]:
    """Returns restaurants where the given field contains the query string."""
    restaurants = _load_restaurants()
    return [
        Restaurant(**r)
        for r in restaurants
        if query.lower() in r[field].lower()
    ]

def search_by_name(name: str) -> List[Restaurant]:
    """Search restaurants by name."""
    return _search_by_field("name", name)

def search_by_cuisine(cuisine: str) -> List[Restaurant]:
    """Search restaurants by cuisine."""
    return _search_by_field("cuisine", cuisine)