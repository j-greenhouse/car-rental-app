with rental as (
    select * from {{ ref('stg_rental_agreement') }}
)

select
    rental_id,
    customer_id,
    vehicle_id,
    pickup_branch_id,
    dropoff_branch_id,
    starting_mileage,
    return_mileage,
    status,
    booking_channel,
    base_rental_cost,
    late_fee,
    total_cost,
    cast(format_date('%Y%m%d', date(starting_rental_date)) as int64) as rental_start_date_id,
    cast(format_date('%Y%m%d', date(expected_return_date)) as int64) as expected_return_date_id,
    case when actual_return_date is not null
        then cast(format_date('%Y%m%d', date(actual_return_date)) as int64)
        else null
    end as actual_return_date_id,
    starting_rental_date,
    expected_return_date,
    actual_return_date
from rental