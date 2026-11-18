-- Warns when the return date precedes the pickup date in source data
-- (greatest(..., 1) in fact_rental_agreement would otherwise mask this).
{{ config(severity='warn') }}

select
    rental_id,
    starting_rental_date,
    expected_return_date,
    actual_return_date
from {{ ref('fact_rental_agreement') }}
where date(coalesce(actual_return_date, expected_return_date)) < date(starting_rental_date)
