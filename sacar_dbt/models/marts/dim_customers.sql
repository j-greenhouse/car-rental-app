with customer as (
    select * from {{ ref('stg_customers') }}
),

tiers as (
    select * from {{ ref('subscription_tiers') }}
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.drivers_license,
    c.subscription_tier,
    c.signup_date,
    c.city,
    c.state,
    t.discount_rate,
    t.late_fee_multiplier
from customer c
left join tiers t
    on c.subscription_tier = t.tier_name