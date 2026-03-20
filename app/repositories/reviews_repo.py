from pathlib import Path
import json, os
from typing import List, Dict, Any

PATH = Path(__file__).resolve().parents[1] / "data" / "reviews.json"

def load_all_reviews() -> List[Dict[str, Any]]:
    if not PATH.exists():
        return []
    
    with PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_all_reviews(reviews: List[Dict[str, Any]]) -> None:
    tmp = PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    os.replace(tmp, PATH)

def get_next_review_id(reviews: List[Dict[str, Any]]) -> int:
    if not reviews:
        return 1
    return max(review["review_id"] for review in reviews ) + 1