from pathlib import Path
import json
import os
from typing import List, Dict, Any

# Path to the notifications JSON file in the data folder
NOTIFICATIONS_PATH = Path(__file__).resolve().parents[1] / "data" / "notifications.json"

def get_notifications_path(override: Path = None) -> Path:
    """
    Returns the path to the notifications JSON file.
    Allows overriding the path for testing purposes.

    Args:
        override (Path, optional): A custom path to use instead of the default.

    Returns:
        Path: The path to the notifications JSON file.
    """
    return override if override else NOTIFICATIONS_PATH

def load_all_notifications(override: Path = None) -> List[Dict[str, Any]]:
    path = get_notifications_path(override)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_all_notifications(notifications: List[Dict[str, Any]], override: Path = None) -> None:
    path = get_notifications_path(override)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(notifications, f, ensure_ascii=False, indent=2)
    os.replace(tmp,path)
    