from pydantic import BaseModel
from typing import List, Optional

class CreateDiscountRequest(BaseModel):
    code: str
    percentage: float
    expiry: str  # format: YYYY-MM-DD
    assigned_to: List[str]  # list of usernames

class DiscountResponse(BaseModel):
    code_id: str
    code: str
    percentage: float
    expiry: str
    assigned_to: List[str]
    used_by: List[str]