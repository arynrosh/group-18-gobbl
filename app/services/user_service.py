# validates input and ensures uniqueness, before saving

from fastapi import HTTPException
from app.repositories.users_repo import load_all_users, save_all_users
from app.schemas.user import RegisterRequest

VALID_ROLES = {"customer", "restaurant_owner", "driver", "admin"}

def validate_input(payload: RegisterRequest) -> None:
    if len(payload.username.strip()) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if "@" not in payload.email or "." not in payload.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if not any(ch.isdigit() for ch in payload.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number")
    if payload.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Role must be one of: {VALID_ROLES}")

def ensure_unique(payload: RegisterRequest) -> None:
    users = load_all_users()
    username = payload.username.strip().lower()
    email = payload.email.strip().lower()
    for u in users:
        if u.get("username", "").lower() == username:
            raise HTTPException(status_code=409, detail="Username already taken")
        if u.get("email", "").lower() == email:
            raise HTTPException(status_code=409, detail="Email already registered")

def register_user(payload: RegisterRequest) -> dict:
    validate_input(payload)
    ensure_unique(payload)
    users = load_all_users()
    new_user = {
        "username": payload.username.strip(),
        "email": payload.email.strip(),
        "password": payload.password,
        "role": payload.role
    }
    users.append(new_user)
    save_all_users(users)
    return {"username": new_user["username"], "email": new_user["email"], "role": new_user["role"]}