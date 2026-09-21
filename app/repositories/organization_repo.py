from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.organization import Branch, Customers, Employees
from app.models.operations import Rental_Agreement, Accident
from typing import List

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, email: str, first_name: str, last_name: str, drivers_license: str, subscription_tier: str | None = None, signup_date=None, city: str | None = None, state: str | None = None) -> Customers:
        """Create a new customer."""
        customer = Customers(
            email=email,
            first_name=first_name,
            last_name=last_name,
            drivers_license=drivers_license,
            subscription_tier=subscription_tier,
            signup_date=signup_date,
            city=city,
            state=state
        )
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def create_branch(self, street_address: str, city: str, state: str, zip_code: int, region: str | None = None) -> Branch:
        """Create a new branch location."""
        branch = Branch(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            region=region
        )
        self.db.add(branch)
        self.db.commit()
        self.db.refresh(branch)
        return branch

    def create_employee(self, first_name: str, last_name: str, role: str, email: str, branchid: int) -> Employees:
        """Create a new employee."""
        employee = Employees(
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
            branchid=branchid
        )
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_branch_by_address(self, street_address: str, city: str, state: str) -> Branch | None:
        """Fetch a branch by its street address, city, and state."""
        return self.db.query(Branch).filter(
            Branch.street_address == street_address,
            Branch.city == city,
            Branch.state == state
        ).first()

    def get_customer_by_id(self, customer_id: int) -> Customers | None:
        """Fetch a customer by their ID."""
        return self.db.query(Customers).filter(Customers.customerid == customer_id).first()

    def get_customer_by_email(self, email: str) -> Customers | None:
        """Fetch a customer by their email."""
        return self.db.query(Customers).filter(Customers.email == email).first()

    def get_customer_by_license(self, drivers_license: str) -> Customers | None:
        """Fetch a customer by their driver's license number."""
        return self.db.query(Customers).filter(Customers.drivers_license == drivers_license).first()

    def get_all_branches(self) -> List[Branch]:
        """Fetch all branch locations."""
        return self.db.query(Branch).all()

    def get_all_employees(self) -> List[Employees]:
        """Fetch all employees."""
        return self.db.query(Employees).all()

    def get_branch_revenue(self, branch_id: int) -> dict:
        """Aggregate total rentals and revenue for a branch."""
        result = self.db.query(
            func.count(Rental_Agreement.rentalid).label("total_rentals"),
            func.coalesce(func.sum(Rental_Agreement.total_cost), 0).label("total_revenue")
        ).filter(Rental_Agreement.pickup_branchid == branch_id).one()
        return {
            "branchid": branch_id,
            "total_rentals": result.total_rentals,
            "total_revenue": float(result.total_revenue)
        }

    def get_customer_summary(self, customer_id: int) -> dict | None:
        """Aggregate rental and accident stats for a customer."""
        customer = self.db.query(Customers).filter(Customers.customerid == customer_id).first()
        if not customer:
            return None
        rental_stats = self.db.query(
            func.count(Rental_Agreement.rentalid).label("total_rentals"),
            func.coalesce(func.sum(Rental_Agreement.total_cost), 0).label("total_spend")
        ).filter(Rental_Agreement.customerid == customer_id).one()
        accident_count = self.db.query(func.count(Accident.accidentid))\
            .join(Rental_Agreement, Accident.rentalid == Rental_Agreement.rentalid)\
            .filter(Rental_Agreement.customerid == customer_id)\
            .scalar()
        return {
            "customerid": customer.customerid,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "drivers_license": customer.drivers_license,
            "total_rentals": rental_stats.total_rentals,
            "total_spend": float(rental_stats.total_spend),
            "total_accidents": accident_count
        }