from fastapi import APIRouter, Depends
from app.api.deps import get_ops_service, require_service_key
from app.services.operations_service import OperationsService
from app.schemas.operations import RentalCreate, RentalOut, RentalReturn, MaintenanceCreate, MaintenanceOut, MaintenanceComplete, AccidentCreate, AccidentOut
from datetime import datetime

router = APIRouter()

@router.post("/rent", response_model=RentalOut, summary="Rent a car to a customer")
def rent_a_car(
    body: RentalCreate,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.rent_car(body.customerid, body.vehicleid, body.pickup_branchid, body.dropoff_branchid, body.starting_mileage, body.starting_rental_date, body.expected_return_date, body.booking_channel)

@router.get("/vehicles/{vehicle_id}/accidents", response_model=list[AccidentOut], summary="Get accident history for a vehicle")
def get_accident_history(
    vehicle_id: int,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_vehicle_accident_history(vehicle_id)

@router.get("/vehicles/{vehicle_id}/maintenance", response_model=list[MaintenanceOut], summary="Get maintenance history for a vehicle")
def get_maintenance_history(
    vehicle_id: int,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_vehicle_maintenance_history(vehicle_id)

@router.put("/rentals/{rental_id}/return", response_model=RentalOut, summary="Return a rented vehicle")
def return_car(
    rental_id: int,
    body: RentalReturn,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.return_car(rental_id, body.return_mileage, body.actual_return_date)

@router.put("/maintenance/{maintenance_id}/complete", response_model=MaintenanceOut, summary="Mark a maintenance record as complete")
def complete_maintenance(
    maintenance_id: int,
    body: MaintenanceComplete,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.complete_maintenance(maintenance_id, body.date_completed)

@router.post("/accidents", response_model=AccidentOut, summary="Record a vehicle accident")
def record_accident(
    body: AccidentCreate,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.log_accident(body.vehicleid, body.rentalid, body.description, body.date_occured)

@router.get("/rentals/overdue", response_model=list[RentalOut], summary="Get all overdue rentals")
def get_overdue_rentals(
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_overdue_rentals()

@router.get("/customers/{customer_id}/rentals", response_model=list[RentalOut], summary="Get rental history for a customer")
def get_rental_history(
    customer_id: int,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_customer_rental_history(customer_id)

@router.get("/rentals/{rental_id}", response_model=RentalOut, summary="Get details for a specific rental")
def get_rental(
    rental_id: int,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_rental_details(rental_id)

@router.post("/maintenance", response_model=MaintenanceOut, summary="Record a vehicle maintenance entry")
def record_maintenance(
    body: MaintenanceCreate,
    service: OperationsService = Depends(get_ops_service),
    api_key: str = Depends(require_service_key)
):
    return service.log_maintenance(body.vehicleid, body.type, body.description, body.cost, body.mileage_at_service, body.accidentid, body.date_completed)