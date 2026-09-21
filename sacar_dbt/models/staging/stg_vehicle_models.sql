with source as (
    select * from {{ source('sacar_raw', 'vehicle_models') }}
)

select
    modelid as model_id,
    make,
    model,
    year,
    body_type,
    fuel_type,
    base_daily_rate
from source
qualify row_number() over (partition by modelid order by modelid) = 1