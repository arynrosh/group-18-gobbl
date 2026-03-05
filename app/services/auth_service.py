from fastapi import HTTPException, status
from app.auth.jwt_handler import create_access_token

# temp placeholder - will replace with real DB query after Task 1.1 merges.
FAKE_USERS = {
    "alice": {"password": "password123", "role": "customer"},
    "bob":   {"password": "securepass",  "role": "restaurant_owner"},
    "dave":  {"password": "driverpass",  "role": "driver"},
    "admin": {"password": "adminpass",   "role": "admin"},
}

def login_user(username: str, password: str) -> dict:
    # Validates credentials and returns a JWT token dict if correct.

    user = FAKE_USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


def get_user_info(current_user: dict) -> dict:
    # Extracts username and role from JWT payload
    return {
        "username": current_user.get("sub"),
        "role": current_user.get("role")
    }

