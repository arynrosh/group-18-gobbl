# Payment router, handles the simulated payment processing endpoint

from fastapi import APIRouter, Depends
from app.schemas.payment import PaymentRequest, PaymentResponse
from app.services.payment_service import process_payment
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/process", response_model=PaymentResponse)
def process(payload: PaymentRequest, current_user: dict = Depends(get_current_user)):
    # Only authenticated users can process payments
    return process_payment(payload)