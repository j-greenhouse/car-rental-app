
with source as (
    select * from {{ source('sacar_raw', 'rental_agreement') }}
)

select
    rentalid as rental_id,
    customerid as customer_id,
    vehicleid as vehicle_id,
    pickup_branchid as pickup_branch_id,
    dropoff_branchid as dropoff_branch_id,
    starting_mileage,
    return_mileage,
    status,
    booking_channel,
    base_rental_cost,
    late_fee,
    total_cost,
    starting_rental_date,
    expected_return_date,
    actual_return_date
from source
qualify row_number() over (partition by rentalid order by rentalid) = 1
