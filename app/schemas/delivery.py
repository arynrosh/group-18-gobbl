from pydantic import BaseModel, Field

#defined but not used (yet)
class Driver(BaseModel):
    id: int
    name: str
    status: str
    driver_distance: float

class DriverDistanceUpdate(BaseModel):
    driver_distance: float = Field(..., ge=0)

class DriverStatusUpdate(BaseModel):
    status: str