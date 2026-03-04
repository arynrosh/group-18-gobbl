import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "changeme-use-a-real-secret-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
   # Creates a signed JWT token containing the given data
   # Always adds an expiry time to the payload
   
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
   # Raises JWTError if the token is invalid/expired
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_username_from_token(token: str) -> str | None:
    try:
        return decode_token(token).get("sub")
    except JWTError:
        return None


def get_role_from_token(token: str) -> str | None:
    # Returns the role from a token, or None if invalid
    try:
        return decode_token(token).get("role")
    except JWTError:
        return None


def is_token_expired(token: str) -> bool:
    # Returns True if the token is expired or invalid, false if still valid
    try:
        decode_token(token)
        return False
    except JWTError:
        return True
