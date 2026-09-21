from pydantic import BaseModel

class VehicleModelCreate(BaseModel):
    make: str
    model: str
    year: int
    body_type: str
    fuel_type: str
    base_daily_rate: float | None = None

class VehicleModelOut(VehicleModelCreate):
    modelid: int

    model_config = {"from_attributes": True}

class VehicleCreate(BaseModel):
    branchid: int
    modelid: int
    color: str
    vin: str
    license_plate: str
    mileage: int

class VehicleOut(VehicleCreate):
    vehicleid: int
    model_info: VehicleModelOut
    status: str

    model_config = {"from_attributes": True}
