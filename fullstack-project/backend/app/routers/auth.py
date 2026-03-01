from fastapi import APIRouter
from schemas.auth_schemas import RegisterRequest
from services.auth_services import register_user
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/Register", status_code = 201)
def register(payload: RegisterRequest):
    register_user(payload)
    return { "message": "User created successfully"}
