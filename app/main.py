from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import fleet, organization, operations

app = FastAPI(title="Super Awesome Car Rentals API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(fleet.router, prefix="/fleet", tags=["Fleet"])
app.include_router(organization.router, prefix="/organization", tags=["Organization"])
app.include_router(operations.router, prefix="/operations", tags=["Operations"])

@app.get("/")
def root():
    return {"message": "Welcome to the Super Awesome Car Rentals API"}