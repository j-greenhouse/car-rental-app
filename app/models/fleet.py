from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, BigInteger, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.operations import Rental_Agreement, Maintenance, Accident

class Vehicle_Models(Base):
    __tablename__ = "vehicle_models"

    modelid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    make: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    body_type: Mapped[Optional[str]] = mapped_column(String(255))
    fuel_type: Mapped[Optional[str]] = mapped_column(String(255))
    base_daily_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))

    # Reference to Vehicle
    vehicles: Mapped[List["Vehicle"]] = relationship("Vehicle", back_populates="model_info")

class Vehicle(Base):
    __tablename__ = "vehicle"

    vehicleid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    branchid: Mapped[int] = mapped_column(BigInteger, ForeignKey("branch.branchid"))
    modelid: Mapped[int] = mapped_column(BigInteger, ForeignKey("vehicle_models.modelid"))
    color: Mapped[Optional[str]] = mapped_column(String(100))
    vin: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    license_plate: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    mileage: Mapped[int] = mapped_column(BigInteger, default=0)
    status: Mapped[str] = mapped_column(String(100), default="Available")

    # Relationships - "Branch" is a string to avoid import errors
    model_info: Mapped["Vehicle_Models"] = relationship("Vehicle_Models", back_populates="vehicles")
    branch: Mapped["Branch"] = relationship("Branch", back_populates="vehicles")
    rentals: Mapped[List["Rental_Agreement"]] = relationship("Rental_Agreement", back_populates="vehicle")
    maintenance_records: Mapped[List["Maintenance"]] = relationship("Maintenance", back_populates="vehicle")
    accidents: Mapped[List["Accident"]] = relationship("Accident", back_populates="vehicle")
