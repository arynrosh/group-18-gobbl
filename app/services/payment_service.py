# Validates card details and simulates gateway approval
import uuid
from datetime import datetime
from fastapi import HTTPException
from app.schemas.payment import PaymentRequest
from app.repositories.payments_repo import load_all_payments, save_all_payments
from app.repositories.order_repo import load_all_orders
from app.services.cost_service import TAX_RATE, DELIVERY_FEE

CARD_NUMBER_LENGTH = 16
CVV_LENGTH = 3


def _validate_card_number(card_number: str) -> None:
    digits = card_number.replace(" ", "")
    if not digits.isdigit() or len(digits) != CARD_NUMBER_LENGTH:
        raise HTTPException(status_code=400, detail=f"Card number must be {CARD_NUMBER_LENGTH} digits")


def _validate_expiry(expiry: str) -> None:
    try:
        month, year = expiry.split("/")
        exp_month = int(month)
        exp_year = int("20" + year)
        now = datetime.now()
        if exp_month < 1 or exp_month > 12:
            raise HTTPException(status_code=400, detail="Invalid expiry month")
        if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
            raise HTTPException(status_code=400, detail="Card has expired")
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="Expiry must be in MM/YY format")


def _validate_cvv(cvv: str) -> None:
    if not cvv.isdigit() or len(cvv) != CVV_LENGTH:
        raise HTTPException(status_code=400, detail=f"CVV must be {CVV_LENGTH} digits")


def validate_card(payload: PaymentRequest) -> None:
    _validate_card_number(payload.card_number)
    _validate_expiry(payload.expiry)
    _validate_cvv(payload.cvv)


def process_payment(payload: PaymentRequest) -> dict:
    validate_card(payload)

    # Verify the order exists
    orders = load_all_orders()
    order = next((o for o in orders if o.get("order_id") == payload.order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {payload.order_id} not found")

    items = order.get("items", [])
    if not items:
        raise HTTPException(status_code=400, detail="Cannot pay for an empty order")
    subtotal = round(sum(item["order_value"] * item["quantity"] for item in items), 2)
    tax = round(subtotal * TAX_RATE, 2)
    amount = round(subtotal + tax + DELIVERY_FEE, 2)

    transaction_id = str(uuid.uuid4())
    record = {
        "transaction_id": transaction_id,
        "order_id": payload.order_id,
        "amount": amount,
        "status": "approved",
        "timestamp": datetime.now().isoformat()
    }

    payments = load_all_payments()
    payments.append(record)
    save_all_payments(payments)

    return {
        "order_id": payload.order_id,
        "status": "approved",
        "message": "Payment approved",
        "transaction_id": transaction_id
    }


def get_payment_by_order(order_id: str) -> dict:
    payments = load_all_payments()
    for p in payments:
        if p.get("order_id") == order_id:
            return p
    raise HTTPException(status_code=404, detail="No payment found for this order")


def get_payment_by_transaction(transaction_id: str) -> dict:
    payments = load_all_payments()
    for p in payments:
        if p.get("transaction_id") == transaction_id:
            return p
    raise HTTPException(status_code=404, detail="Transaction not found")