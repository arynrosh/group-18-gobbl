import json
from pathlib import Path
from typing import List, Dict, Any
import os

ORDER_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.json"
ORDERITEM_PATH = Path(__file__).resolve().parents[1] / "data" / "OrderItem.json"
STATUS_PATH = Path(__file__).resolve().parents[1] / "data" / "status.json"

def load_all_orders() -> List[Dict[str, Any]]:
    if not ORDER_PATH.exists():
        return []
    with ORDER_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_all_orders(orders: List[Dict[str, Any]]) -> None:
    tmp = ORDER_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ORDER_PATH)

def load_all_orderitems() -> List[Dict[str, Any]]:
    if not ORDERITEM_PATH.exists():
        return []
    with ORDERITEM_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_all_orderitems(orderitems: List[Dict[str, Any]]) -> None:
    tmp = ORDERITEM_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(orderitems, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ORDERITEM_PATH)

def load_all_status() -> List[Dict[str, Any]]:
    if not STATUS_PATH.exists():
        return []
    with STATUS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_all_orders(status: List[Dict[str, Any]]) -> None:
    tmp = STATUS_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATUS_PATH)