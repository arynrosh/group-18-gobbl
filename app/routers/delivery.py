from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth.dependencies import require_roles
from app.repositories.drivers_repo import load_all_drivers
from app.services.delivery_service import (
    update_driver_distance,
    update_driver_status,
    auto_assign_driver,
    assign_driver_to_order,
)
from app.schemas.delivery import DriverDistanceUpdate, DriverStatusUpdate

router = APIRouter(prefix="/delivery", tags=["delivery"])

@router.get("/drivers")
def get_all_driver(
    current_user: dict = Depends(require_roles("restaurant_owner"))
):
    drivers = load_all_drivers()
    return {"drivers": drivers}

@router.put("/drivers/{driver_id}/driver_distance")
def update_distance(
    driver_id: int,
    driver_data: DriverDistanceUpdate,
    current_user: dict = Depends(require_roles("driver")),
):
    updated_driver = update_driver_distance(driver_id, driver_data)
    return {"message": "Driver distance updated", "driver": updated_driver}

@router.put("/drivers/{driver_id}/driver_status")
def update_status(
    driver_id: int,
    driver_data: DriverStatusUpdate,
    current_user: dict = Depends(require_roles("driver")),
):
    updated_driver = update_driver_status(driver_id, driver_data)
    return {"message": "Driver status updated", "driver": updated_driver}

@router.post("/orders/{order_id}/auto-assign-driver")
def auto_assign(
    order_id: str,
    current_user: dict = Depends(require_roles("restaurant_owner")),
):
    return auto_assign_driver(order_id)

@router.post("/orders/{order_id}/assign/{driver_id}")
def assign_driver(
    order_id:str,
    driver_id:int,
    current_user: dict = Depends(require_roles("restaurant_owner")),
):
    return assign_driver_to_order(order_id, driver_id)