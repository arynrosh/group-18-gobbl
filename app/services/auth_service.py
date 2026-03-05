from fastapi import HTTPException, status
from app.auth.jwt_handler import create_access_token
from app.repositories.users_repo import load_all_users

def login_user(username: str, password: str) -> dict:
    # looks up user in JSON store and returns JWT if credentials match
    users = load_all_users()
    user = next((u for u in users if u.get("username", "").lower() == username.lower()), None)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

def get_user_info(current_user: dict) -> dict:
    # extracts username and role from JWT payload
    return {
        "username": current_user.get("sub"),
        "role": current_user.get("role")
    }
