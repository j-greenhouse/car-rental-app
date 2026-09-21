from app.repositories.fleet_repo import FleetRepository
from app.models.fleet import Vehicle, Vehicle_Models
from fastapi import HTTPException
from datetime import datetime

class FleetService:
    def __init__(self, repo: FleetRepository):
        self.repo = repo

    def get_all_available_cars(self, branch_id: int | None = None) -> list[Vehicle]:
        """Returns only cars that are ready to be rented, optionally filtered by branch."""
        return self.repo.get_all_vehicles(status="Available", branch_id=branch_id)

    def get_vehicle_details(self, vehicle_id: int) -> Vehicle:
        """Fetch detailed information about a specific vehicle."""
        vehicle = self.repo.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    def add_vehicle_to_fleet(self, branchid: int, modelid: int, color: str, vin: str, license_plate: str, mileage: int) -> Vehicle:
        """Add a new vehicle to the fleet."""
        return self.repo.create_vehicle(branchid, modelid, color, vin, license_plate, mileage)
    
    def get_vehicles_available_in_range(self, start_date: datetime, end_date: datetime, vehicle_id: int | None = None) -> list[Vehicle]:
        """Fetch vehicles available over a date range, optionally filtered to a specific vehicle."""
        return self.repo.get_vehicles_available_in_range(start_date, end_date, vehicle_id)

    def get_vehicles_overdue_maintenance(self, branch_id: int) -> list[Vehicle]:
        """Fetch vehicles at a branch that are 5000+ miles past their last service."""
        return self.repo.get_vehicles_overdue_maintenance(branch_id)

    def add_model_definition(self, make: str, model: str, year: int, body_type: str, fuel_type: str, base_daily_rate: float | None = None) -> Vehicle_Models:
        """Add a new vehicle model."""
        return self.repo.create_vehicle_model(make, model, year, body_type, fuel_type, base_daily_rate)