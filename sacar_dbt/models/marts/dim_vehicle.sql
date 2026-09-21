with vehicle as (
    select * from {{ ref('stg_vehicle') }}
),

vehicle_models as (
    select * from {{ ref('stg_vehicle_models') }}
)

select
    v.vehicle_id,
    v.branch_id,
    v.color,
    v.vin,
    v.license_plate,
    v.mileage,
    v.status,
    m.model_id,
    m.make,
    m.model,
    m.year,
    m.body_type,
    m.fuel_type,
    m.base_daily_rate
from vehicle v
left join vehicle_models m
    on v.model_id = m.model_id