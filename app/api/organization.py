from fastapi import APIRouter, Depends
from app.api.deps import get_org_service, require_service_key
from app.services.organization_service import OrganizationService
from app.schemas.organization import BranchOut, BranchCreate, EmployeeCreate, EmployeeOut, CustomerCreate, CustomerOut, BranchRevenueSummary, CustomerSummary

router = APIRouter()

@router.post("/customers", response_model=CustomerOut, summary="Register a new customer")
def register_customer(
    body: CustomerCreate,
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.register_customer(body.email, body.first_name, body.last_name, body.drivers_license, body.subscription_tier, body.signup_date, body.city, body.state)

@router.get("/customers/{customer_id}", response_model=CustomerOut, summary="Get details for a specific customer")
def get_customer(
    customer_id: int,
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_customer_details(customer_id)

@router.get("/employees", response_model=list[EmployeeOut], summary="List all employees")
def get_employees(
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_all_employees()

@router.get("/branches", response_model=list[BranchOut], summary="List all rental locations")
def get_branches(
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_all_locations()

@router.post("/employees", response_model=EmployeeOut, summary="Create a new employee")
def create_employee(
    body: EmployeeCreate,
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.create_employee(body.first_name, body.last_name, body.role, body.email, body.branchid)

@router.get("/branches/{branch_id}/revenue", response_model=BranchRevenueSummary, summary="Get total revenue for a branch")
def get_branch_revenue(
    branch_id: int,
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_branch_revenue(branch_id)

@router.get("/customers/{customer_id}/summary", response_model=CustomerSummary, summary="Get rental and accident summary for a customer")
def get_customer_summary(
    customer_id: int,
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.get_customer_summary(customer_id)

@router.post("/branches", response_model=BranchOut, summary="Create a new rental branch")
def create_branch(
    body: BranchCreate,
    service: OrganizationService = Depends(get_org_service),
    api_key: str = Depends(require_service_key)
):
    return service.add_new_location(body.street_address, body.city, body.state, body.zip_code, body.region)