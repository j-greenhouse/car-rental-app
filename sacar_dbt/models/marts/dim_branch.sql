with branch as (
    select * from {{ ref('stg_branch') }}
)

select
    branch_id,
    street_address,
    city,
    state,
    zip_code,
    region
from branch