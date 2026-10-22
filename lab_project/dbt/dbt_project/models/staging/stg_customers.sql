{{ config(schema='dds', materialized='view') }}
select
    trim(customer_id::text) as customer_id,
    trim(customer_name::text) as customer_name,
    trim(city::text) as city,
    trim(region::text) as region,
    cast(customer_updated_at as timestamp) as customer_updated_at
from {{ source('stage_dimensions', 'customers') }}
