# sacar_dbt

dbt project that transforms raw car rental data (branches, customers, vehicles, rental agreements) into a star schema for analytics, sourced from the `sacar-portfolio` BigQuery project.

## Structure

```
models/
├── staging/    pulls necessary tables from sacar_raw source (stg_branch, stg_customers, stg_vehicle, stg_vehicle_models, stg_rental_agreement)
└── marts/      
    ├── dim_branch
    ├── dim_customer
    ├── dim_vehicle
    ├── dim_date
    └── fact_rental_agreement
```

Sources are declared in [`models/staging/_sacar__sources.yml`](models/staging/_sacar__sources.yml) (`sacar_raw` schema) and mart tests/descriptions live in [`models/marts/_sacar__marts.yml`](models/marts/_sacar__marts.yml).

## Seeds

- `subscription_tiers.csv` — subscription tier discount and late fee rates, joined into `dim_customer`.

## Setup

**1. Configure your dbt profile**

This project targets BigQuery (`profile: sacar_dbt`, database `sacar-portfolio`). Set up a `profiles.yml` entry with a service account key or `gcloud` auth — see [dbt-bigquery setup](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup).

**2. Install dependencies and seed reference data**

```bash
dbt deps
dbt seed
```

**3. Run and test**

```bash
dbt run
dbt test
```
