from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RentalCreate(BaseModel):
    customerid: int
    vehicleid: int
    pickup_branchid: int
    dropoff_branchid: Optional[int] = None
    starting_mileage: int
    starting_rental_date: datetime
    expected_return_date: datetime
    booking_channel: Optional[str] = None

class RentalOut(RentalCreate):
    rentalid: int
    status: str
    base_rental_cost: Optional[float] = None
    total_cost: Optional[float] = None
    late_fee: Optional[float] = None

    model_config = {"from_attributes": True}

class MaintenanceCreate(BaseModel):
    vehicleid: int
    accidentid: Optional[int] = None
    type: str
    description: str
    cost: float
    mileage_at_service: int
    date_completed: Optional[datetime] = None

class MaintenanceOut(MaintenanceCreate):
    maintenanceid: int
    date_in: datetime
    date_completed: Optional[datetime] = None

    model_config = {"from_attributes": True}

class RentalReturn(BaseModel):
    return_mileage: int
    actual_return_date: datetime

class MaintenanceComplete(BaseModel):
    date_completed: datetime

class AccidentCreate(BaseModel):
    vehicleid: int
    rentalid: int
    description: str
    date_occured: datetime

class AccidentOut(AccidentCreate):
    accidentid: int

    model_config = {"from_attributes": True}
