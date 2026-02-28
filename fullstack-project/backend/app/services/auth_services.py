from schemas.auth_schemas import RegisterRequest
from fastapi import HTTPException

def validate_registration_input(payload: RegisterRequest) -> None: 
  if len(payload.username.strip()) < 3: 
    raise HTTPException(status_code = 400, detail= "Username must be atleast 3 characters long; retry")

  email = payload.email.strip()
  if "@" not in email or "." not in email:
    raise HTTPException(status_code = 400, detail= "Invalid email format; retry")

  if len(payload.password) < 8: 
    raise HTTPException(status_code = 400, detail= "Password must be at least 8 characters")
  if not any(ch.isdigit() for ch in payload.password):
    raise HTTPException(status_code=400, detail= "password must contain atleast one number; retry)
