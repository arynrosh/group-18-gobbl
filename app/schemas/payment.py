# Pydantic schemas for payment request and response validation

from pydantic import BaseModel

class PaymentRequest(BaseModel):
    order_id: str
    cardholder_name: str
    card_number: str
    expiry: str
    cvv: str

class PaymentResponse(BaseModel):
    order_id: str
      # approved or rejected
    status: str
    message: str
    transaction_id: str