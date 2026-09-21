from sqlalchemy import String, BigInteger, ForeignKey, DateTime, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import TYPE_CHECKING, List, Optional
import datetime

if TYPE_CHECKING:
    from app.models.organization import Customers
    from app.models.fleet import Vehicle


class Rental_Agreement(Base):
    __tablename__ = "rental_agreement"

    rentalid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    customerid: Mapped[int] = mapped_column(BigInteger, ForeignKey("customers.customerid"))
    vehicleid: Mapped[int] = mapped_column(BigInteger, ForeignKey("vehicle.vehicleid"))
    pickup_branchid: Mapped[int] = mapped_column(BigInteger, ForeignKey("branch.branchid"))
    dropoff_branchid: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("branch.branchid"), nullable=True)
    
    starting_mileage: Mapped[Optional[int]] = mapped_column(BigInteger)
    return_mileage: Mapped[Optional[int]] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(100), default="Active")
    base_rental_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    total_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    late_fee: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    booking_channel: Mapped[Optional[str]] = mapped_column(String(50))

    starting_rental_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow
    )
    expected_return_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    actual_return_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    customer: Mapped["Customers"] = relationship("Customers", back_populates="rentals")
    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="rentals")
    accidents: Mapped[List["Accident"]] = relationship("Accident", back_populates="rental")

class Maintenance(Base):
    __tablename__ = "maintenance"

    maintenanceid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    vehicleid: Mapped[int] = mapped_column(BigInteger, ForeignKey("vehicle.vehicleid"))
    accidentid: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("accident.accidentid"), nullable=True)
    type: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    mileage_at_service: Mapped[Optional[int]] = mapped_column(BigInteger)
    date_in: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow
    )
    date_completed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="maintenance_records")
    accident: Mapped[Optional["Accident"]] = relationship("Accident", back_populates="maintenance_record")

class Accident(Base):
    __tablename__ = "accident"

    accidentid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    vehicleid: Mapped[int] = mapped_column(BigInteger, ForeignKey("vehicle.vehicleid"))
    rentalid: Mapped[int] = mapped_column(BigInteger, ForeignKey("rental_agreement.rentalid"))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_occured: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))

    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="accidents")
    rental: Mapped["Rental_Agreement"] = relationship("Rental_Agreement", back_populates="accidents")
    maintenance_record: Mapped[Optional["Maintenance"]] = relationship("Maintenance", back_populates="accident", uselist=False)