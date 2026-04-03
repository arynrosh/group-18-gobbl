# validates input and ensures uniqueness, before saving

from fastapi import HTTPException
from app.repositories.users_repo import load_all_users, save_all_users
from app.schemas.user import RegisterRequest
from typing import List

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

def create_diet_restrictions(role: str) -> None:
    if role == "customer":
        return True
    else:
        False

def validate_input(payload: RegisterRequest) -> None:
    # All input validation
    _validate_username(payload.username)
    _validate_email(payload.email)
    _validate_password(payload.password)
    _validate_role(payload.role)
    #if create_diet_restrictions(payload.role):
    #    payload.diet_restrictions = []


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
    if create_diet_restrictions(payload.role):
        new_user = {
             "username": payload.username.strip(),
            "email": payload.email.strip(),
            "password": payload.password,
            "role": payload.role,
            "diet_restrictions": List[str]
        }
    else:
        new_user = {
            "username": payload.username.strip(),
            "email": payload.email.strip(),
            "password": payload.password,
            "role": payload.role
        }
    users.append(new_user)
    save_all_users(users)
    return {"username": new_user["username"], "email": new_user["email"], "role": new_user["role"]}

def get_diet_restrictions_or_404(username: str, users: list[dict]) -> dict:
    user = next((u for u in users if u.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {username} not found")
    else:
        try:
            user.get("diet_restrictions")
        except NameError:
            raise HTTPException(status_code=400, detail=f"User {username} does not have diet_restrictions")
    return user

def add_diet_restriction(username: str, restriction: str) -> dict:
    users = load_all_users()
    user = get_diet_restrictions_or_404(username, users)

    user["diet_restrictions"].append(restriction)
    save_all_users(users)
    return user

def remove_diet_restriction(username: str, restriction: str) -> dict:
    users = load_all_users()
    user = get_diet_restrictions_or_404(username, users)

    original_count = len(user["diet_restrictions"])
    user["diet_restrictions"] = [i for i in user["diet_restrictions"] if i.get("restriction") != restriction]

    if len(user["diet_restrictions"]) == original_count:
        raise HTTPException(status_code=404, detail=f"Diet Restriction {restriction} not found in user's listed restrictions")

    save_all_users(users)
    return user



