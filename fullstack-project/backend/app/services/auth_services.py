from schemas.auth_schemas import RegisterRequest
from fastapi import HTTPException
from repositories.users_repo import load_all_users, save_all_users

def validate_registration_input(payload: RegisterRequest) -> None: 
  if len(payload.username.strip()) < 3: 
    raise HTTPException(status_code = 400, detail= "Username must be atleast 3 characters long; retry")

  email = payload.email.strip()
  if "@" not in email or "." not in email:
    raise HTTPException(status_code = 400, detail= "Invalid email format; retry")

  if len(payload.password) < 8: 
    raise HTTPException(status_code = 400, detail= "Password must be at least 8 characters")
  if not any(ch.isdigit() for ch in payload.password):
    raise HTTPException(status_code=400, detail= "password must contain atleast one number; retry")

def ensure_unique_user(payload: RegisterRequest) -> None: 
  users = load_all_users()

  username = payload.username.strip().lower()
  email = payload.email.strip().lower()
  for u in users: 
    if u.get("username", "").strip().lower() == username:
      raise HTTPException(status_code=409, detail= "This Username already exists with an account")

    if u.get("email", "").strip().lower() == email:
      raise HTTPException(status_code=409, detail = "This email already exists with an account")

def register_user(payload: RegisterRequest) -> None:
  validate_registration_input(payload)
  ensure_unique_user(payload)

  user = load_all_users()

  new_user = {
    "username": payload.username.strip(),
    "email": payload.email.strip(),
    "password": payload.password,
}
  user.append(new_user)
  save_all_users(users)
  
  
