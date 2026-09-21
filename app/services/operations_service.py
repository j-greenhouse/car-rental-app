from app.repositories.operations_repo import OperationsRepository
from app.repositories.fleet_repo import FleetRepository
from app.repositories.organization_repo import OrganizationRepository
from app.models.operations import Rental_Agreement, Accident, Maintenance
from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Optional
import math

LATE_FEE_PER_DAY = 70

# Subscription tier -> (rate discount on base rental cost, multiplier applied to late fees)
SUBSCRIPTION_TIERS = {
    "None":    {"discount": 0.00, "late_fee_multiplier": 1.00},
    "Basic":   {"discount": 0.10, "late_fee_multiplier": 1.00},
    "Premium": {"discount": 0.20, "late_fee_multiplier": 0.50},
}

class OperationsService:
    def __init__(self, ops_repo: OperationsRepository, fleet_repo: FleetRepository, org_repo: OrganizationRepository):
        self.ops_repo = ops_repo
        self.fleet_repo = fleet_repo
        self.org_repo = org_repo

    def rent_car(self, customer_id: int, vehicle_id: int, pickup_branch_id: int, dropoff_branch_id: Optional[int] = None, starting_mileage: int = 0, start_date: datetime = None, end_date: datetime = None, booking_channel: Optional[str] = None) -> Rental_Agreement:
        """Process a car rental request."""
        # 1. Check if the car is actually available
        vehicle = self.fleet_repo.get_vehicle_by_id(vehicle_id)
        if not vehicle or vehicle.status != "Available":
            raise HTTPException(status_code=400, detail="Vehicle is not available for rental")

        if not vehicle.model_info or vehicle.model_info.base_daily_rate is None:
            raise HTTPException(status_code=400, detail="Vehicle model does not have a base daily rate set")

        customer = self.org_repo.get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # 2. Calculate the base rental cost from the model's daily rate and rental length,
        # discounted per the customer's subscription tier
        tier = SUBSCRIPTION_TIERS.get(customer.subscription_tier, SUBSCRIPTION_TIERS["None"])
        rental_days = max(math.ceil((end_date - start_date).total_seconds() / 86400), 1)
        base_rental_cost = float(vehicle.model_info.base_daily_rate) * rental_days * (1 - tier["discount"])

        # 3. Create the rental record (total_cost starts equal to the base cost; late fees are added on return)
        rental = self.ops_repo.create_rental(customer_id, vehicle_id, pickup_branch_id, dropoff_branch_id, starting_mileage, start_date, end_date, base_rental_cost, base_rental_cost, booking_channel)

        # 4. Update the car status so no one else can rent it
        self.fleet_repo.update_vehicle_status(vehicle_id, "Rented")

        return rental

    def get_vehicle_accident_history(self, vehicle_id: int) -> list[Accident]:
        """Fetch all accidents for a vehicle."""
        return self.ops_repo.get_accidents_by_vehicle(vehicle_id)

    def get_vehicle_maintenance_history(self, vehicle_id: int) -> list[Maintenance]:
        """Fetch all maintenance records for a vehicle."""
        return self.ops_repo.get_maintenance_by_vehicle(vehicle_id)

    def return_car(self, rental_id: int, return_mileage: int, actual_return_date: datetime) -> Rental_Agreement:
        """Process a car return."""
        existing = self.ops_repo.get_rental_by_id(rental_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Rental not found")

        # Business Rule: returning a vehicle after its expected return date incurs a late fee
        late_fee = 0.0
        expected = existing.expected_return_date
        if expected is not None:
            actual = actual_return_date
            if actual.tzinfo is None:
                actual = actual.replace(tzinfo=timezone.utc)
            if expected.tzinfo is None:
                expected = expected.replace(tzinfo=timezone.utc)
            if actual > expected:
                late_days = math.ceil((actual - expected).total_seconds() / 86400)
                tier = SUBSCRIPTION_TIERS.get(
                    existing.customer.subscription_tier if existing.customer else None,
                    SUBSCRIPTION_TIERS["None"],
                )
                late_fee = late_days * LATE_FEE_PER_DAY * tier["late_fee_multiplier"]

        rental = self.ops_repo.return_rental(rental_id, return_mileage, actual_return_date, late_fee)
        # Business Rule: Returning a car makes it available for new rentals
        self.fleet_repo.update_vehicle_status(rental.vehicleid, "Available")
        return rental

    def complete_maintenance(self, maintenance_id: int, date_completed: datetime) -> Maintenance:
        """Mark maintenance as complete and return the vehicle to service."""
        record = self.ops_repo.complete_maintenance(maintenance_id, date_completed)
        if not record:
            raise HTTPException(status_code=404, detail="Maintenance record not found")
        # Business Rule: Completing maintenance returns the vehicle to available status
        self.fleet_repo.update_vehicle_status(record.vehicleid, "Available")
        return record

    def log_accident(self, vehicle_id: int, rental_id: int, description: str, date_occured: datetime) -> Accident:
        """Record an accident and mark the vehicle as under repair."""
        accident = self.ops_repo.create_accident(vehicle_id, rental_id, description, date_occured)
        # Business Rule: A vehicle involved in an accident is immediately taken out of service until repaired
        self.fleet_repo.update_vehicle_status(vehicle_id, "Under Repair")
        return accident

    def get_rental_details(self, rental_id: int) -> Rental_Agreement:
        """Fetch detailed information about a specific rental agreement."""
        rental = self.ops_repo.get_rental_by_id(rental_id)
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")
        return rental

    def get_customer_rental_history(self, customer_id: int) -> list[Rental_Agreement]:
        """Fetch full rental history for a customer."""
        return self.ops_repo.get_rentals_by_customer(customer_id)

    def get_overdue_rentals(self) -> list[Rental_Agreement]:
        """Fetch all active rentals past their expected return date."""
        return self.ops_repo.get_overdue_rentals()

    def log_maintenance(self, vehicle_id: int, type: str, description: str, cost: float, mileage_at_service: int, accident_id: Optional[int] = None, date_completed: Optional[datetime] = None) -> Maintenance:
        """Record a maintenance entry, optionally linked to an accident."""
        return self.ops_repo.create_maintenance(vehicle_id, type, description, cost, mileage_at_service, accident_id, date_completed)