from fastapi import HTTPException, status
from app.schemas.order import Order, OrderItem, Status
from app.repositories.order_repo import (
    load_all_orders, save_all_orders,
    load_all_orderitems, save_all_orderitems,
    load_all_status, save_all_status
)
from app.services.order_notification_service import (
    notify_order_placed,
    notify_out_for_delivery,
    notify_order_delivered,
    notify_order_delayed
)

from app.services.menu_service import get_menu_item

def _get_order_or_404(order_id: str, orders: list[dict]) -> dict:
    order = next((o for o in orders if o.get("order_id") == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order


def _get_status_or_404(order_id: str) -> dict:
    statuses = load_all_status()
    record = next((s for s in statuses if s.get("order_id") == order_id), None)
    if not record:
        raise HTTPException(status_code=404, detail=f"Status for order {order_id} not found")
    return record


def create_order(order_id: str, customer_id: str, restaurant_id: int, delivery_distance: float, delivery_time: float,assigned_driver_id: int) -> dict:
    orders = load_all_orders()
    if any(o.get("order_id") == order_id for o in orders):
        raise HTTPException(status_code=409, detail="Order ID already exists")

    new_order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "restaurant_id": restaurant_id,
        "delivery_distance": delivery_distance,
        "delivery_time": delivery_time,
        "assigned_driver_id": assigned_driver_id,
        "items": [],
        "sent": False
    }
    orders.append(new_order)
    save_all_orders(orders)

    statuses = load_all_status()
    statuses.append({"order_id": order_id, "current": "pending", "complete": False})
    save_all_status(statuses)

    return new_order


def add_to_order(order_id: str, restaurant_id: int, food_item: str, quantity: int) -> dict:
    orders = load_all_orders()
    order = _get_order_or_404(order_id, orders)

    if order.get("sent"):
        raise HTTPException(status_code=400, detail="Cannot modify order after it has been sent")
    
    menu_item = get_menu_item(food_item, restaurant_id)

    if order["restaurant_id"] != menu_item["restaurant_id"]:
        raise HTTPException(
            status_code=400,
            detail="Item does not belong to this order's restaurant"
        )        

    new_item = {
        "food_item": menu_item["food_item"],
        "quantity": quantity,
        "order_value": menu_item["order_value"],
    }

    order["items"].append(new_item)
    save_all_orders(orders)
    return order


def remove_from_order(order_id: str, food_item: str) -> dict:
    orders = load_all_orders()
    order = _get_order_or_404(order_id, orders)

    if order.get("sent"):
        raise HTTPException(status_code=400, detail="Cannot modify order after it has been sent")

    original_count = len(order["items"])
    order["items"] = [i for i in order["items"] if i.get("food_item") != food_item]

    if len(order["items"]) == original_count:
        raise HTTPException(status_code=404, detail=f"Item {food_item} not found in order")

    save_all_orders(orders)
    return order


def send_order(order_id: str) -> dict:
    orders = load_all_orders()
    order = _get_order_or_404(order_id, orders)

    if order.get("sent"):
        raise HTTPException(status_code=400, detail="Order has already been sent")

    if not order.get("items"):
        raise HTTPException(status_code=400, detail="Cannot send an empty order")

    order["sent"] = True
    save_all_orders(orders)

    statuses = load_all_status()
    record = next((s for s in statuses if s.get("order_id") == order_id), None)
    if record:
        record["current"] = "sent"
    save_all_status(statuses)

    return order


def get_order(order_id: str) -> dict:
    orders = load_all_orders()
    return _get_order_or_404(order_id, orders)


def update_status(order_id: str, msg: str) -> dict:
    statuses = load_all_status()
    record = _get_status_or_404(order_id)

    if record.get("complete"):
        raise HTTPException(status_code=400, detail="Cannot update status of a completed order")

    record["current"] = msg
    save_all_status(statuses)

    orders = load_all_orders()
    order = _get_order_or_404(order_id, orders)
    customer_id = order["customer_id"]
    restaurant_id = order["restaurant_id"]

    if msg == "placed":
        notify_order_placed(order_id, customer_id, restaurant_id)
    elif msg == "out for delivery":
        notify_out_for_delivery(order_id, customer_id, restaurant_id, "your driver")
    elif msg == "delayed":
        notify_order_delayed(order_id, customer_id, restaurant_id, 0)

    return record


def complete_order_status(order_id: str) -> dict:
    statuses = load_all_status()
    record = _get_status_or_404(order_id)

    record["complete"] = True
    save_all_status(statuses)

    orders = load_all_orders()
    order = _get_order_or_404(order_id, orders)
    notify_order_delivered(order_id, order["customer_id"], order["restaurant_id"])
    return record


def get_status(order_id: str) -> dict:
    return _get_status_or_404(order_id)