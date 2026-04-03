from pydantic import BaseModel
from typing import List, Optional

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str
    diet_restrictions: Optional[List[str]] = None
    
class UserResponse(BaseModel):
    username: str
    email: str
    role: str
