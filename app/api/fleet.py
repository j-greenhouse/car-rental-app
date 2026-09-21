from fastapi import APIRouter, Depends, Query
from app.api.deps import get_fleet_service, require_service_key
from app.services.fleet_service import FleetService
from app.schemas.fleet import VehicleCreate, VehicleModelCreate, VehicleOut, VehicleModelOut
from datetime import datetime

router = APIRouter()

@router.get("/vehicles", response_model=list[VehicleOut], summary="List all available vehicles")
def list_available_vehicles(
    branch_id: int | None = Query(default=None, description="Filter by branch location"),
    service: FleetService = Depends(get_fleet_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_all_available_cars(branch_id=branch_id)

@router.post("/vehicles", response_model=VehicleOut, summary="Add a new vehicle to the fleet")
def add_vehicle(
    body: VehicleCreate,
    service: FleetService = Depends(get_fleet_service),
    api_key: str = Depends(require_service_key)
):
    return service.add_vehicle_to_fleet(body.branchid, body.modelid, body.color, body.vin, body.license_plate, body.mileage)

@router.get("/vehicles/available", response_model=list[VehicleOut], summary="Get vehicles available over a date range")
def get_vehicles_available_in_range(
    start_date: datetime = Query(..., description="Start of the requested rental period"),
    end_date: datetime = Query(..., description="End of the requested rental period"),
    vehicle_id: int | None = Query(default=None, description="Optionally check a specific vehicle"),
    service: FleetService = Depends(get_fleet_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_vehicles_available_in_range(start_date, end_date, vehicle_id)

@router.get("/vehicles/maintenance-overdue/{branch_id}", response_model=list[VehicleOut], summary="Get vehicles overdue for maintenance at a branch")
def get_vehicles_overdue_maintenance(
    branch_id: int,
    service: FleetService = Depends(get_fleet_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_vehicles_overdue_maintenance(branch_id)

@router.get("/vehicles/{vehicle_id}", response_model=VehicleOut, summary="Get details for a specific vehicle")
def get_vehicle(
    vehicle_id: int,
    service: FleetService = Depends(get_fleet_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_vehicle_details(vehicle_id)

@router.post("/models", response_model=VehicleModelOut, summary="Define a new vehicle model")
def create_model(
    body: VehicleModelCreate,
    service: FleetService = Depends(get_fleet_service),
    api_key: str = Depends(require_service_key)
):
    return service.add_model_definition(body.make, body.model, body.year, body.body_type, body.fuel_type, body.base_daily_rate)