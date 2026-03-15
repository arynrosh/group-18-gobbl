from pydantic import BaseModel

class DriverLocationUpdate(BaseModel):
    x: float
    y: float

class DriverStatusUpdate(BaseModel):
    status: str