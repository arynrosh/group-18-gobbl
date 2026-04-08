from fastapi import APIRouter, Depends
from app.services.order_service import (
    create_order, add_to_order, remove_from_order,
    send_order, get_order, get_orders, update_status,
    complete_order_status, get_status,
    make_my_mystery_bag
)
from app.auth.dependencies import get_current_user, require_roles
from app.schemas.order import MysteryBagRequest

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", status_code=201)
def create_new_order(
    order_id: str,
    restaurant_id: int,
    delivery_distance: float,
    delivery_time: float = None,
    current_user: dict = Depends(require_roles("customer"))
):
    return create_order(
        order_id=order_id,
        customer_id=current_user["sub"],
        restaurant_id=restaurant_id,
        delivery_distance=delivery_distance,
        delivery_time=delivery_time,
    )

@router.get("/{order_id}")
def get_order_by_id(order_id: str, current_user: dict = Depends(get_current_user)):
    return get_order(order_id)

@router.get("")
def get_my_orders(current_user: dict = Depends(get_current_user)):
    return get_orders(current_user["sub"])

@router.post("/{order_id}/items")
def add_item(
    order_id: str,
    restaurant_id: int,
    food_item: str,
    quantity: int,
    current_user: dict = Depends(require_roles("customer"))
):
    return add_to_order(order_id, restaurant_id, food_item, quantity)


@router.delete("/{order_id}/items/{food_item}")
def remove_item(
    order_id: str,
    food_item: str,
    current_user: dict = Depends(require_roles("customer"))
):
    return remove_from_order(order_id, food_item)


@router.put("/{order_id}/send")
def submit_order(order_id: str, current_user: dict = Depends(require_roles("customer"))):
    return send_order(order_id)


@router.get("/{order_id}/status")
def get_order_status(order_id: str, current_user: dict = Depends(get_current_user)):
    return get_status(order_id)


@router.put("/{order_id}/status")
def update_order_status(
    order_id: str,
    msg: str,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    return update_status(order_id, msg)


@router.put("/{order_id}/complete")
def complete_order(
    order_id: str,
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    return complete_order_status(order_id)

@router.post("/{order_id}/mystery-bag")
def make_mystery_bag(
    order_id: str,
    mystery_data: MysteryBagRequest,
    current_user: dict = Depends(require_roles("customer"))
):
    mystery_bag = make_my_mystery_bag(order_id, mystery_data)

    return {"message": "Mystery bag added to order", "mystery_bag": mystery_bag}