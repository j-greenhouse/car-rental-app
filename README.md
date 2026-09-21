# Super Awesome Car Rentals API

A REST API for managing a car rental business — fleet inventory, branch locations, employees, customers, rentals, maintenance, and accident records.

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL
- **Validation:** Pydantic v2
- **Server:** Uvicorn

## Project Structure

```
app/
├── api/            # Route handlers (fleet, organization, operations)
├── services/       # Business logic
├── repositories/   # Database queries
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic request/response schemas
└── core/           # Config, database session, security
```

## Setup

**1. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
API_KEY=your-secret-api-key
```

**4. Run the server**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Authentication

All endpoints require an `x-api-key` header matching the value set in your `.env`:

```
x-api-key: your-secret-api-key
```

Requests without a valid key return `401 Unauthorized`.

## API Endpoints

### Fleet — `/fleet`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/fleet/vehicles` | List all available vehicles (optional `branch_id` query param) |
| `POST` | `/fleet/vehicles` | Add a vehicle to the fleet |
| `GET` | `/fleet/vehicles/available` | Get vehicles available over a date range (`start_date`, `end_date` required; optional `vehicle_id`) |
| `GET` | `/fleet/vehicles/maintenance-overdue/{branch_id}` | Get vehicles overdue for maintenance at a branch |
| `GET` | `/fleet/vehicles/{vehicle_id}` | Get details for a specific vehicle |
| `POST` | `/fleet/models` | Define a new vehicle model |

### Organization — `/organization`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/organization/branches` | List all branch locations |
| `POST` | `/organization/branches` | Create a new branch |
| `POST` | `/organization/customers` | Register a new customer |
| `GET` | `/organization/customers/{customer_id}` | Get details for a specific customer |
| `POST` | `/organization/employees` | Create a new employee |
| `GET` | `/organization/employees` | List all employees |
| `GET` | `/organization/branches/{branch_id}/revenue` | Get total revenue for a branch |
| `GET` | `/organization/customers/{customer_id}/summary` | Get rental and accident summary for a customer |

### Operations — `/operations`

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/operations/rent` | Rent a vehicle to a customer |
| `PUT` | `/operations/rentals/{rental_id}/return` | Return a rented vehicle |
| `GET` | `/operations/rentals/overdue` | Get all overdue rentals |
| `GET` | `/operations/rentals/{rental_id}` | Get details for a specific rental |
| `GET` | `/operations/customers/{customer_id}/rentals` | Get rental history for a customer |
| `POST` | `/operations/accidents` | Record a vehicle accident |
| `GET` | `/operations/vehicles/{vehicle_id}/accidents` | Get accident history for a vehicle |
| `POST` | `/operations/maintenance` | Record a vehicle maintenance entry |
| `PUT` | `/operations/maintenance/{maintenance_id}/complete` | Mark a maintenance record as complete |
| `GET` | `/operations/vehicles/{vehicle_id}/maintenance` | Get maintenance history for a vehicle |

## Data Model

```
Branch ──< Employees
Branch ──< Vehicle ──< Rental_Agreement >── Customer
                   ──< Maintenance
                   ──< Accident >── Rental_Agreement
Vehicle_Models ──< Vehicle
```
