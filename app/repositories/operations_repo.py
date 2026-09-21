from sqlalchemy.orm import Session
from app.models.operations import Rental_Agreement, Accident, Maintenance
from typing import List, Optional
from datetime import datetime

class OperationsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_rental(self, customer_id: int, vehicle_id: int, pickup_branch_id: int, dropoff_branch_id: int, starting_mileage: int, start_date: datetime, end_date: datetime, base_rental_cost: float | None = None, total_cost: float | None = None, booking_channel: str | None = None) -> Rental_Agreement:
        """Create a new rental agreement."""
        rental = Rental_Agreement(
            customerid=customer_id,
            vehicleid=vehicle_id,
            pickup_branchid=pickup_branch_id,
            dropoff_branchid=dropoff_branch_id,
            starting_mileage=starting_mileage,
            status="Active",
            starting_rental_date=start_date,
            expected_return_date=end_date,
            base_rental_cost=base_rental_cost,
            total_cost=total_cost,
            booking_channel=booking_channel
        )
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def get_rental_by_id(self, rental_id: int) -> Rental_Agreement | None:
        """Fetch a rental agreement by its ID."""
        return self.db.query(Rental_Agreement).filter(Rental_Agreement.rentalid == rental_id).first()

    def get_active_rentals_by_customer(self, customer_id: int) -> List[Rental_Agreement]:
        """Fetch active rentals for a customer."""
        return self.db.query(Rental_Agreement).filter(
            Rental_Agreement.customerid == customer_id,
            Rental_Agreement.status == "Active"
        ).all()

    def get_rentals_by_customer(self, customer_id: int) -> List[Rental_Agreement]:
        """Fetch all rentals for a customer, most recent first."""
        return self.db.query(Rental_Agreement)\
            .filter(Rental_Agreement.customerid == customer_id)\
            .order_by(Rental_Agreement.starting_rental_date.desc())\
            .all()

    def get_overdue_rentals(self) -> List[Rental_Agreement]:
        """Fetch all active rentals past their expected return date."""
        return self.db.query(Rental_Agreement)\
            .filter(
                Rental_Agreement.status == "Active",
                Rental_Agreement.expected_return_date < datetime.utcnow()
            )\
            .order_by(Rental_Agreement.expected_return_date.asc())\
            .all()

    def get_accidents_by_vehicle(self, vehicle_id: int) -> List[Accident]:
        """Fetch all accidents for a vehicle, most recent first."""
        return self.db.query(Accident)\
            .filter(Accident.vehicleid == vehicle_id)\
            .order_by(Accident.date_occured.desc())\
            .all()

    def get_maintenance_by_vehicle(self, vehicle_id: int) -> List[Maintenance]:
        """Fetch all maintenance records for a vehicle, most recent first."""
        return self.db.query(Maintenance)\
            .filter(Maintenance.vehicleid == vehicle_id)\
            .order_by(Maintenance.date_in.desc())\
            .all()

    def return_rental(self, rental_id: int, return_mileage: int, actual_return_date: datetime, late_fee: float = 0.0) -> Rental_Agreement | None:
        """Mark a rental as completed, record return details, and apply any late fee."""
        rental = self.db.query(Rental_Agreement).filter(Rental_Agreement.rentalid == rental_id).first()
        if rental:
            rental.status = "Completed"
            rental.return_mileage = return_mileage
            rental.actual_return_date = actual_return_date
            rental.late_fee = late_fee
            rental.total_cost = float(rental.base_rental_cost or 0) + late_fee
            self.db.commit()
            self.db.refresh(rental)
        return rental

    def complete_maintenance(self, maintenance_id: int, date_completed: datetime) -> Maintenance | None:
        """Mark a maintenance record as completed."""
        record = self.db.query(Maintenance).filter(Maintenance.maintenanceid == maintenance_id).first()
        if record:
            record.date_completed = date_completed
            self.db.commit()
            self.db.refresh(record)
        return record

    def create_accident(self, vehicle_id: int, rental_id: int, description: str, date_occured: datetime) -> Accident:
        """Record a new accident."""
        accident = Accident(
            vehicleid=vehicle_id,
            rentalid=rental_id,
            description=description,
            date_occured=date_occured
        )
        self.db.add(accident)
        self.db.commit()
        self.db.refresh(accident)
        return accident

    def create_maintenance(self, vehicle_id: int, type: str, description: str, cost: float, mileage_at_service: int, accident_id: Optional[int] = None, date_completed: Optional[datetime] = None) -> Maintenance:
        """Record a maintenance entry, optionally linked to an accident."""
        record = Maintenance(
            vehicleid=vehicle_id,
            accidentid=accident_id,
            type=type,
            description=description,
            cost=cost,
            mileage_at_service=mileage_at_service,
            date_completed=date_completed
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record