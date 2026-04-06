from fastapi import APIRouter, Depends
from app.schemas.payment import PaymentRequest, PaymentResponse
from app.services.payment_service import process_payment, get_payment_by_order, get_payment_by_transaction
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/process", response_model=PaymentResponse)
def process(payload: PaymentRequest, current_user: dict = Depends(get_current_user)):
    return process_payment(payload, current_user["sub"])

@router.get("/order/{order_id}")
def get_by_order(order_id: str, current_user: dict = Depends(get_current_user)):
    return get_payment_by_order(order_id)

@router.get("/transaction/{transaction_id}")
def get_by_transaction(transaction_id: str, current_user: dict = Depends(get_current_user)):
    return get_payment_by_transaction(transaction_id)