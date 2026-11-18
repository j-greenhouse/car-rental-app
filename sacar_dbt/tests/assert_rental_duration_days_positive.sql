-- Fails if any rental has a duration below 1 day.
select
    rental_id,
    rental_duration_days
from {{ ref('fact_rental_agreement') }}
where rental_duration_days < 1
