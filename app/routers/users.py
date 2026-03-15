from fastapi import APIRouter
from app.schemas.user import RegisterRequest, UserResponse
from app.services.user_service import register_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest):
    #creates a new user account with validated unique credentials
    return register_user(payload)
