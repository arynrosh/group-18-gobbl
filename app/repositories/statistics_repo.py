from pathlib import Path
import csv
from typing import List, Dict, Any
from app.repositories.order_repo import load_all_orders

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "food_delivery.csv"

def load_all_orders() -> List[Dict[str, Any]]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]