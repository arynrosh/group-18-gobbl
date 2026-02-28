from pathlib import Path 
import json, os
from typing import Any

DATA_PATH = Path(_file_).resolve().parents[1]/ "data"/ "users.json"/
"""
Load users from the JSON file 
Returns empty list if the file doesn't exist or is invalid
"""
def load_all_users -> List[Dict[str, any]]:
  if not DATA_PATH.exists():
    return []

with DATA_PATH.open("r", encoding="utf-8") as f: 
  return json.load(f)

def save_all_users(users: List[Dict[str, Any]]) -> None:
  tmp = DATA_PATH.with.suffix(".tmp")
  with tmp.open("w", encoding="utf-8") as f: 
    json.dump(users, f, ensure_ascii = False, indent=2)
  os.replace(tmp, DATA_PATH)
  
