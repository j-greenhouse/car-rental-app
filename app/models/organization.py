from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import datetime

if TYPE_CHECKING:
    from app.models.operations import Rental_Agreement

class Branch(Base):
    __tablename__ = "branch"

    branchid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    street_address: Mapped[Optional[str]] = mapped_column(String(500))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))
    zip_code: Mapped[Optional[int]] = mapped_column(BigInteger)
    region: Mapped[Optional[str]] = mapped_column(String(255))

    managerid: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("employees.employeeid", use_alter=True, name="fk_branch_manager")
    )

    # Relationships - "Employees" and "Vehicle" are strings
    employees: Mapped[List["Employees"]] = relationship(
        "Employees", back_populates="branch", foreign_keys="Employees.branchid"
    )
    vehicles: Mapped[List["Vehicle"]] = relationship("Vehicle", back_populates="branch")

class Employees(Base):
    __tablename__ = "employees"

    employeeid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    
    branchid: Mapped[int] = mapped_column(BigInteger, ForeignKey("branch.branchid"))
    
    branch: Mapped["Branch"] = relationship(
        "Branch", back_populates="employees", foreign_keys=[branchid]
    )

class Customers(Base):
    __tablename__ = "customers"

    customerid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    drivers_license: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    subscription_tier: Mapped[Optional[str]] = mapped_column(String(50))
    signup_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    city: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))

    rentals: Mapped[List["Rental_Agreement"]] = relationship("Rental_Agreement", back_populates="customer")