# Handles saving and retrieving payment methods for users.
# CVV is never stored and card number is masked to last 4 digits only.

import uuid
from fastapi import HTTPException
from app.repositories.payment_methods_repo import load_all_payment_methods, save_all_payment_methods
from app.schemas.payment_method import SavePaymentMethodRequest

CARD_NUMBER_LENGTH = 16

def save_payment_method(username: str, cardholder_name: str, card_number: str, expiry: str) -> dict:
    # Validate card number before saving
    digits = card_number.replace(" ", "")
    if not digits.isdigit() or len(digits) != CARD_NUMBER_LENGTH:
        raise HTTPException(status_code=400, detail=f"Card number must be {CARD_NUMBER_LENGTH} digits")

    last_four = digits[-4:]
    method_id = str(uuid.uuid4())

    record = {
        "method_id": method_id,
        "username": username,
        "cardholder_name": payload.cardholder_name,
        "last_four": last_four,
        "expiry": payload.expiry
    }

    methods = load_all_payment_methods()
    methods.append(record)
    save_all_payment_methods(methods)

    return record

def get_payment_methods(username: str) -> list:
    # Returns all saved cards for a given user
    methods = load_all_payment_methods()
    return [m for m in methods if m.get("username") == username]

def delete_payment_method(username: str, method_id: str) -> dict:
    # Deletes a saved card, only the owner can delete their own card
    methods = load_all_payment_methods()
    match = next((m for m in methods if m.get("method_id") == method_id), None)

    if not match:
        raise HTTPException(status_code=404, detail="Payment method not found")
    if match.get("username") != username:
        raise HTTPException(status_code=403, detail="You can only delete your own payment methods")

    updated = [m for m in methods if m.get("method_id") != method_id]
    save_all_payment_methods(updated)
    return {"message": "Payment method deleted"}