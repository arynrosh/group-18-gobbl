from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    username: str
    role: str