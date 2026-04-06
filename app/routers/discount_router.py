from fastapi import APIRouter, Depends
from app.schemas.discount import CreateDiscountRequest, DiscountResponse
from app.services.discount_service import create_discount, get_my_discounts, get_all_discounts
from app.auth.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/discounts", tags=["discounts"])

@router.post("", response_model=DiscountResponse, status_code=201)
def create_new_discount(
    payload: CreateDiscountRequest,
    current_user: dict = Depends(require_roles("admin"))
):
    return create_discount(
        code=payload.code,
        percentage=payload.percentage,
        expiry=payload.expiry,
        assigned_to=payload.assigned_to
    )

@router.get("/my-codes", response_model=list[DiscountResponse])
def get_user_discounts(current_user: dict = Depends(require_roles("customer"))):
    return get_my_discounts(current_user["sub"])


@router.get("", response_model=list[DiscountResponse])
def get_discounts(current_user: dict = Depends(require_roles("admin"))):
    return get_all_discounts()