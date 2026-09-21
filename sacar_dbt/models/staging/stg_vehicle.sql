with source as (
    select * from {{ source('sacar_raw', 'vehicle') }}
)

select
    vehicleid as vehicle_id,
    branchid as branch_id,
    modelid as model_id,
    color,
    vin,
    license_plate,
    mileage,
    status
from source
qualify row_number() over (partition by vehicleid order by vehicleid) = 1