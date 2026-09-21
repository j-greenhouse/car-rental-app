from app.repositories.organization_repo import OrganizationRepository
from app.models.organization import Customers, Branch, Employees
from fastapi import HTTPException

class OrganizationService:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def register_customer(self, email: str, first_name: str, last_name: str, drivers_license: str, subscription_tier: str | None = None, signup_date=None, city: str | None = None, state: str | None = None) -> Customers:
        """Register a new customer with the provided details."""
        # Business Rule: Don't allow duplicate emails
        if self.repo.get_customer_by_email(email):
            raise HTTPException(status_code=400, detail="Customer with this email already exists")

        if self.repo.get_customer_by_license(drivers_license):
            raise HTTPException(status_code=400, detail="Customer with this driver's license already exists")

        return self.repo.create_customer(email, first_name, last_name, drivers_license, subscription_tier, signup_date, city, state)

    def get_customer_details(self, customer_id: int) -> Customers:
        """Fetch detailed information about a specific customer."""
        customer = self.repo.get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    def add_new_location(self, street_address: str, city: str, state: str, zip_code: int, region: str | None = None) -> Branch:
        # Business Rule: No two branches can share the same street address, city, and state
        existing = self.repo.get_branch_by_address(street_address, city, state)
        if existing:
            raise HTTPException(status_code=400, detail="A branch already exists at this address")
        return self.repo.create_branch(street_address, city, state, zip_code, region)

    def create_employee(self, first_name: str, last_name: str, role: str, email: str, branchid: int) -> Employees:
        """Create a new employee."""
        return self.repo.create_employee(first_name, last_name, role, email, branchid)

    def get_branch_revenue(self, branch_id: int) -> dict:
        """Get total rentals and revenue for a branch."""
        return self.repo.get_branch_revenue(branch_id)

    def get_customer_summary(self, customer_id: int) -> dict:
        """Get rental and accident stats for a customer."""
        result = self.repo.get_customer_summary(customer_id)
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return result

    def get_all_locations(self) -> list[Branch]:
        """Fetch all branch locations."""
        return self.repo.get_all_branches()

    def get_all_employees(self) -> list[Employees]:
        """Fetch all employees."""
        return self.repo.get_all_employees()