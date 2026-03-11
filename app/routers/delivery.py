from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth.dependencies import require_roles
from app.services.delivery_service import (
    update_driver_location,
    update_driver_status,
    