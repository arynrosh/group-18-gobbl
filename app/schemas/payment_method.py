from pydantic import BaseModel

class SavePaymentMethodRequest(BaseModel):
    cardholder_name: str
    card_number: str
    expiry: str

class PaymentMethodResponse(BaseModel):
    method_id: str
    cardholder_name: str
    last_four: str
    expiry: str