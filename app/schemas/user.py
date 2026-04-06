from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str
    
class UserResponse(BaseModel):
    username: str
    email: str
    role: str
