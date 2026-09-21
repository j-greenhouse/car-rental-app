with source as (
    select * from {{ source('sacar_raw', 'customers') }}
)

select
    customerid as customer_id,
    first_name,
    last_name,
    email,
    drivers_license,
    subscription_tier,
    signup_date,
    city,
    state
from source
qualify row_number() over (partition by customerid order by customerid) = 1
