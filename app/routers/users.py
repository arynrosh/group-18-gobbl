from fastapi import APIRouter, Depends
from app.schemas.user import RegisterRequest, UserResponse
from app.services.user_service import register_user
from app.auth.dependencies import get_current_user, require_roles
from app.services.user_service import (
    add_diet_restriction,
    remove_diet_restriction
)


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest):
    #creates a new user account with validated unique credentials
    return register_user(payload)

@router.post("/{username}/diet_restrictions")
def add_diet_restriction(username: str,
    diet_restriction: str, 
    current_user: dict = Depends(require_roles("customer"))
):
    return add_diet_restriction(username, diet_restriction)

@router.delete("/{username}/diet_restrictions/{diet_restriction}")
def remove_diet_restriction(username: str,
    diet_restriction: str, 
    current_user: dict = Depends(require_roles("customer"))
):
    return remove_diet_restriction(username, diet_restriction)