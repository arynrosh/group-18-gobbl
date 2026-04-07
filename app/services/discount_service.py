# Service layer for discount code management
# Admins create codes and assign them to users
# Customers can apply codes at checkout for a percentage discount

import uuid
from datetime import datetime
from fastapi import HTTPException
from app.repositories.discount_repo import load_all_discounts, save_all_discounts


def create_discount(code: str, percentage: float, expiry: str, assigned_to: list) -> dict:
    # Admin creates a discount code and assigns it to specific users
    if percentage <= 0 or percentage > 100:
        raise HTTPException(status_code=400, detail="Percentage must be between 1 and 100")

    try:
        datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Expiry must be in YYYY-MM-DD format")

    discounts = load_all_discounts()
    if any(d.get("code") == code for d in discounts):
        raise HTTPException(status_code=409, detail="Discount code already exists")

    new_discount = {
        "code_id": str(uuid.uuid4()),
        "code": code,
        "percentage": percentage,
        "expiry": expiry,
        "assigned_to": assigned_to,
        "used_by": []
    }
    discounts.append(new_discount)
    save_all_discounts(discounts)
    return new_discount


def get_my_discounts(username: str) -> list:
    discounts = load_all_discounts()
    today = datetime.now().strftime("%Y-%m-%d")
    result = []
    for d in discounts:
        if username in d.get("assigned_to", []):
            if username not in d.get("used_by", []):
                if d.get("expiry") >= today:
                    result.append(d)
    return result


def get_all_discounts() -> list:
    return load_all_discounts()


def validate_and_apply_discount(code: str, username: str, amount: float) -> float:
    discounts = load_all_discounts()
    today = datetime.now().strftime("%Y-%m-%d")

    discount = next((d for d in discounts if d.get("code") == code), None)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount code not found")

    if username not in discount.get("assigned_to", []):
        raise HTTPException(status_code=403, detail="This discount code was not assigned to you")

    if username in discount.get("used_by", []):
        raise HTTPException(status_code=400, detail="You have already used this discount code")

    if discount.get("expiry") < today:
        raise HTTPException(status_code=400, detail="This discount code has expired")

    percentage = discount.get("percentage", 0)
    discounted_amount = round(amount * (1 - percentage / 100), 2)

    discount["used_by"].append(username)
    save_all_discounts(discounts)

    return discounted_amount