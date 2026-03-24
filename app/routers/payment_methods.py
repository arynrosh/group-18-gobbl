# Payment methods router, handles saving and retrieving cards for users

from fastapi import APIRouter, Depends
from app.schemas.payment_method import SavePaymentMethodRequest, PaymentMethodResponse
from app.services.payment_methods_service import save_payment_method, get_payment_methods, delete_payment_method
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/payment-methods", tags=["payment-methods"])


@router.post("", response_model=PaymentMethodResponse, status_code=201)
def save_method(payload: SavePaymentMethodRequest, current_user: dict = Depends(get_current_user)):
    # Saves a card for the currently logged in user
    return save_payment_method(current_user["sub"],payload.cardholder_name, payload.card_number, payload.expiry)


@router.get("", response_model=list[PaymentMethodResponse])
def get_methods(current_user: dict = Depends(get_current_user)):
    # Returns all saved cards for the currently logged in user
    return get_payment_methods(current_user["sub"])


@router.delete("/{method_id}")
def delete_method(method_id: str, current_user: dict = Depends(get_current_user)):
    # Deletes saved card belonging to the currently logged in user
    return delete_payment_method(current_user["sub"], method_id)