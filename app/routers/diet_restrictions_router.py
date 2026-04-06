from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user, require_roles
from app.services.diet_restrictions_services import (
    add_diet_restriction,
    remove_diet_restriction
)

router = APIRouter(prefix="/diet_restrictions", tags=["diet_restrictions"])

@router.post("/{username}/diet_restrictions")
def add_diet_restriction(
    username: str,
    diet_restriction: str, 
    current_user: dict = Depends(require_roles("customer"))
):
    return add_diet_restriction(username, diet_restriction)

@router.delete("/{username}/diet_restrictions/{diet_restriction}")
def remove_diet_restriction(
    username: str,
    diet_restriction: str, 
    current_user: dict = Depends(require_roles("customer"))
):
    return remove_diet_restriction(username, diet_restriction)