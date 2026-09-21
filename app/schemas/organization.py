from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BranchCreate(BaseModel):
    street_address: str
    city: str
    state: str
    zip_code: int
    region: Optional[str] = None

class BranchOut(BranchCreate):
    branchid: int

    model_config = {"from_attributes": True}

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    role: str
    email: str
    branchid: int

class EmployeeOut(EmployeeCreate):
    employeeid: int

    model_config = {"from_attributes": True}

class CustomerCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    drivers_license: str
    subscription_tier: Optional[str] = None
    signup_date: Optional[datetime] = None
    city: Optional[str] = None
    state: Optional[str] = None

class CustomerOut(CustomerCreate):
    customerid: int

    model_config = {"from_attributes": True}

class BranchRevenueSummary(BaseModel):
    branchid: int
    total_rentals: int
    total_revenue: float

class CustomerSummary(BaseModel):
    customerid: int
    first_name: str
    last_name: str
    email: str
    drivers_license: str
    total_rentals: int
    total_spend: float
    total_accidents: int