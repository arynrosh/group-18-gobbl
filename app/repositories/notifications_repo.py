from pathlib import Path
import json
import os
from typing import List, Dict, Any

# Path to the notifications JSON file in the data folder
NOTIFICATIONS_PATH = Path(__file__).resolve().parents[1] / "data" / "notifications.json"

def load_all_notifications() -> List[Dict[str, Any]]:
    if not NOTIFICATIONS_PATH.exists():
        return []
    with NOTIFICATIONS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_all_notifications(notifications: List[Dict[str, Any]]) -> None:
    tmp = NOTIFICATIONS_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(notifications, f, ensure_ascii=False, indent=2)
    os.replace(tmp, NOTIFICATIONS_PATH)