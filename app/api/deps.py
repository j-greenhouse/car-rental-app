from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

# Core imports
from app.core.db import get_db
from app.core.security import require_service_key

# Repository imports
from app.repositories.fleet_repo import FleetRepository
from app.repositories.organization_repo import OrganizationRepository
from app.repositories.operations_repo import OperationsRepository

# Service imports (We will build these next!)
from app.services.fleet_service import FleetService
from app.services.organization_service import OrganizationService
from app.services.operations_service import OperationsService

# --- Repository Injectors ---
# These provide the "Data Access" layer to your services

def get_fleet_repo(db: Session = Depends(get_db)) -> FleetRepository:
    return FleetRepository(db)

def get_org_repo(db: Session = Depends(get_db)) -> OrganizationRepository:
    return OrganizationRepository(db)

def get_ops_repo(db: Session = Depends(get_db)) -> OperationsRepository:
    return OperationsRepository(db)

# --- Service Injectors ---
# These provide the "Business Logic" layer to your API routes

def get_fleet_service(repo: FleetRepository = Depends(get_fleet_repo)) -> FleetService:
    return FleetService(repo)

def get_org_service(repo: OrganizationRepository = Depends(get_org_repo)) -> OrganizationService:
    return OrganizationService(repo)

def get_ops_service(
    ops_repo: OperationsRepository = Depends(get_ops_repo),
    fleet_repo: FleetRepository = Depends(get_fleet_repo),
    org_repo: OrganizationRepository = Depends(get_org_repo)
) -> OperationsService:
    return OperationsService(ops_repo, fleet_repo, org_repo)

# --- The "One-Stop Shop" Export ---
# Matches your professor's __all__ style
__all__ = [
    "get_db",
    "require_service_key",
    "get_fleet_service",
    "get_org_service",
    "get_ops_service"
]