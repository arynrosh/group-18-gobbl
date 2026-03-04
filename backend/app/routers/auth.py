# from fastapi import APIRouter, Depends, status, HTTPException
# from fastapi.security import HTTPBasicCredentials, HTTPBasic
# from pydantic import BaseModel
# from typing import Dict, Optional, List
# import time

# router = APIRouter(prefix="/auth", tags=[])

from fastapi import APIRouter, status
from schemas.auth_schemas import RegisterRequest
from services.auth_services import register_user
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code = 201)
def register(payload: RegisterRequest):
    result = register_user(payload)
    return { "message": "User created successfully"}