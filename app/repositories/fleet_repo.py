from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.fleet import Vehicle, Vehicle_Models
from app.models.operations import Maintenance, Rental_Agreement
from typing import List, Optional
from datetime import datetime

class FleetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_vehicle_by_id(self, vehicle_id: int) -> Vehicle | None:
        """Fetch a vehicle by its ID."""
        return self.db.query(Vehicle).filter(Vehicle.vehicleid == vehicle_id).first()

    def get_all_vehicles(self, status: str | None = None, branch_id: int | None = None) -> List[Vehicle]:
        """Fetch all vehicles, optionally filtered by status and/or branch."""
        query = self.db.query(Vehicle)
        if status:
            query = query.filter(Vehicle.status == status)
        if branch_id:
            query = query.filter(Vehicle.branchid == branch_id)
        return query.all()

    def update_vehicle_status(self, vehicle_id: int, new_status: str) -> Vehicle | None:
        """Update the status of a vehicle."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if vehicle:
            vehicle.status = new_status
            self.db.commit()
            self.db.refresh(vehicle)
        return vehicle
    
    def create_vehicle(self, branchid: int, modelid: int, color: str, vin: str, license_plate: str, mileage: int) -> Vehicle:
        """Create a new vehicle."""
        vehicle = Vehicle(
            branchid=branchid,
            modelid=modelid,
            vin=vin,
            license_plate=license_plate,
            color=color,
            mileage=mileage,
            status="Available"
        )
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
    
    def get_vehicles_available_in_range(self, start_date: datetime, end_date: datetime, vehicle_id: int | None = None) -> List[Vehicle]:
        """Fetch vehicles with no conflicting active rentals in the given date range."""
        conflicting = (
            self.db.query(Rental_Agreement.vehicleid)
            .filter(
                Rental_Agreement.status == "Active",
                Rental_Agreement.starting_rental_date < end_date,
                Rental_Agreement.expected_return_date > start_date
            )
            .subquery()
        )
        query = self.db.query(Vehicle).filter(Vehicle.vehicleid.not_in(conflicting))
        if vehicle_id:
            query = query.filter(Vehicle.vehicleid == vehicle_id)
        return query.all()

    def get_vehicles_overdue_maintenance(self, branch_id: int) -> List[Vehicle]:
        """Fetch vehicles at a branch that are 5000+ miles past their last service."""
        latest_service = (
            self.db.query(
                Maintenance.vehicleid,
                func.max(Maintenance.mileage_at_service).label("last_service_mileage")
            )
            .group_by(Maintenance.vehicleid)
            .subquery()
        )
        return (
            self.db.query(Vehicle)
            .outerjoin(latest_service, Vehicle.vehicleid == latest_service.c.vehicleid)
            .filter(
                Vehicle.branchid == branch_id,
                Vehicle.mileage - func.coalesce(latest_service.c.last_service_mileage, 0) >= 5000
            )
            .all()
        )

    def create_vehicle_model(self, make: str, model: str, year: int, body_type: str, fuel_type: str, base_daily_rate: float | None = None) -> Vehicle_Models:
        """Create a new vehicle model."""
        new_model = Vehicle_Models(
            make=make,
            model=model,
            year=year,
            body_type=body_type,
            fuel_type=fuel_type,
            base_daily_rate=base_daily_rate
        )
        self.db.add(new_model)
        self.db.commit()
        self.db.refresh(new_model)
        return new_model