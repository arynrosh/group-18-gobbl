# validates input and ensures uniqueness, before saving

from fastapi import HTTPException
from app.repositories.users_repo import load_all_users, save_all_users
from app.schemas.user import RegisterRequest

VALID_ROLES = {"customer", "restaurant_owner", "driver", "admin"}


def _validate_username(username: str) -> None:
    if len(username.strip()) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")


def _validate_email(email: str) -> None:
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")


def _validate_password(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if not any(ch.isdigit() for ch in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number")


def _validate_role(role: str) -> None:
    if role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Role must be one of: {VALID_ROLES}")


def validate_input(payload: RegisterRequest) -> None:
    # All input validation
    _validate_username(payload.username)
    _validate_email(payload.email)
    _validate_password(payload.password)
    _validate_role(payload.role)


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