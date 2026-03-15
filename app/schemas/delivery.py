from pydantic import BaseModel, Field

class DriverDistanceUpdate(BaseModel):
    driver_distance: float = Field(..., ge=0)

class DriverStatusUpdate(BaseModel):
    status: str