# Order fulfillment behind a verified payment record.

from fastapi import HTTPException
from app.repositories.payments_repo import load_all_payments
from app.repositories.fulfillment_repo import load_all_orders, save_all_orders

def fulfill_order(order_id: str) -> dict:
    # Checking that a payment exists for this order before allowing fulfillment
    payments = load_all_payments()
    payment = next((p for p in payments if p.get("order_id") == order_id), None)

    if not payment:
        raise HTTPException(status_code=402, detail="Payment required before order can be fulfilled")

    if payment.get("status") != "approved":
        raise HTTPException(status_code=402, detail="Payment was not approved for this order")

    # Marking order as fulfilled
    orders = load_all_orders()
    existing = next((o for o in orders if o.get("order_id") == order_id), None)

    if existing:
        if existing.get("fulfillment_status") == "fulfilled":
            raise HTTPException(status_code=400, detail="Order has already been fulfilled")
        existing["fulfillment_status"] = "fulfilled"
    else:
        orders.append({"order_id": order_id, "fulfillment_status": "fulfilled"})

    save_all_orders(orders)
    return {"order_id": order_id, "fulfillment_status": "fulfilled"}

def get_fulfillment_status(order_id: str) -> dict:
    # Returns fulfillment status of an order
    orders = load_all_orders()
    record = next((o for o in orders if o.get("order_id") == order_id), None)

    if not record:
        return {"order_id": order_id, "fulfillment_status": "pending"}
    return record