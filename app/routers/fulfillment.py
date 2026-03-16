# Order fulfillment behind verified payment

from fastapi import APIRouter, Depends
from app.services.fulfillment_service import fulfill_order, get_fulfillment_status
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["fulfillment"])


@router.post("/{order_id}/fulfill")
def fulfill(order_id: str, current_user: dict = Depends(get_current_user)):
    # Fulfills an order only if a verified payment exists
    return fulfill_order(order_id)


@router.get("/{order_id}/fulfillment-status")
def fulfillment_status(order_id: str, current_user: dict = Depends(get_current_user)):
    # Returns  current fulfillment status of an order
    return get_fulfillment_status(order_id)