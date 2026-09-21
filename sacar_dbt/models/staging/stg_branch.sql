with source as (
    select * from {{ source('sacar_raw', 'branch') }}
)

select
    branchid as branch_id,
    street_address,
    city,
    state,
    zip_code,
    managerid as manager_id,
    region
from source
qualify row_number() over (partition by branchid order by branchid) = 1