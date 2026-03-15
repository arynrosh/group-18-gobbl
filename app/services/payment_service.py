# Validates card details and simulates gateway approval
import uuid
from datetime import datetime
from fastapi import HTTPException
from app.schemas.payment import PaymentRequest
from app.repositories.payments_repo import load_all_payments, save_all_payments

def validate_card(payload: PaymentRequest) -> None:
    # Card number has to be exactly 16 digits
    if not payload.card_number.replace(" ", "").isdigit() or len(payload.card_number.replace(" ", "")) != 16:
        raise HTTPException(status_code=400, detail="Card number must be 16 digits")

    # Expiry must be MM/YY and not in the past
    try:
        month, year = payload.expiry.split("/")
        exp_month = int(month)
        exp_year = int("20" + year)
        now = datetime.now()
        if exp_month < 1 or exp_month > 12:
            raise HTTPException(status_code=400, detail="Invalid expiry month")
        if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
            raise HTTPException(status_code=400, detail="Card has expired")
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="Expiry must be in MM/YY format")

    # CVV must be exactly 3 digits
    if not payload.cvv.isdigit() or len(payload.cvv) != 3:
        raise HTTPException(status_code=400, detail="CVV must be 3 digits")

    # Amount must be positive
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

def process_payment(payload: PaymentRequest) -> dict:
    validate_card(payload)

    # All valid cards will be approved
    transaction_id = str(uuid.uuid4())
    record = {
        "transaction_id": transaction_id,
        "order_id": payload.order_id,
        "amount": payload.amount,
        "status": "approved",
        "timestamp": datetime.now().isoformat()
    }

    # Save payment record
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
    # Returns the payment record for a given order, or raises 404
    payments = load_all_payments()
    for p in payments:
        if p.get("order_id") == order_id:
            return p
    raise HTTPException(status_code=404, detail="No payment found for this order")

def get_payment_by_transaction(transaction_id: str) -> dict:
    # Returns the payment record for a given transaction ID, or raises 404
    payments = load_all_payments()
    for p in payments:
        if p.get("transaction_id") == transaction_id:
            return p
    raise HTTPException(status_code=404, detail="Transaction not found")
