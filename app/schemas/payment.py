from pydantic import BaseModel

class PaymentRequest(BaseModel):
    order_id: str
    cardholder_name: str
    card_number: str
    expiry: str
    cvv: str
    discount_code: str | None = None

class PaymentResponse(BaseModel):
    order_id: str
    status: str
    message: str
    transaction_id: str