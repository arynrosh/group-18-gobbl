# Validates card details and simulates gateway approval
import uuid
from datetime import datetime
from fastapi import HTTPException
from app.schemas.payment import PaymentRequest

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
    return {
        "order_id": payload.order_id,
        "status": "approved",
        "message": "Payment approved",
        "transaction_id": transaction_id
    }