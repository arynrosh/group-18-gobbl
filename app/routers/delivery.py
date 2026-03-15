from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth.dependencies import require_roles
from app.services.delivery_service import (
    update_driver_location,
    update_driver_status,
    auto_assign_driver,
    assign_driver_to_delivery,
)
from app.schemas.delivery import DriverDistanceUpdate, DriverStatusUpdate

router = APIRouter(prefix="/delivery", tags=["delivery"])

@router.put("/drivers/{driver_id}/distance")
def update_distance(
    driver_id: str,
    body: DriverDistanceUpdate,
    current_user: dict = Depends(require_roles("driver")),
):
    updated_driver = update_driver_location(driver_id, body.driver_distance)
    return {
        "message": "Driver distance updated",
        "driver": updated_driver
    }

@router.put("/drivers/{driver_id}/status")
def update_status(
    driver_id: str,
    body: DriverStatusUpdate,
    current_user: dict = Depends(require_roles("driver")),
):
    updated_driver = update_driver_status(driver_id, body.status)
    return {
        "message": "Driver status updated",
        "driver": updated_driver
    }

@router.post("/deliveries/{delivery_id}/auto-assign")
def auto_assign(
    delivery_id: str,
    current_user: dict = Depends(require_roles("restaurant_owner")),
):
    return auto_assign_driver(delivery_id)

@router.post("/deliveries/{delivery_id}/assign/{driver_id}")
def assign_driver(
    delivery_id:str,
    driver_id:str,
    current_user: dict = Depends(require_roles("restaurant_owner")),
):
    return assign_driver_to_delivery(delivery_id, driver_id)