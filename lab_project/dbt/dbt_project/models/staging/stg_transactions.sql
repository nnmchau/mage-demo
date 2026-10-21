{{ config(schema='dds', materialized='view') }}

select
    trim(cast(transaction_id as text)) as transaction_id,
    cast(transaction_ts as timestamp) as transaction_ts,
    cast(source_updated_at as timestamp) as source_updated_at,
    trim(cast(customer_id as text)) as customer_id,
    trim(cast(product_id as text)) as product_id,
    cast(quantity as integer) as quantity,
    cast(unit_price as numeric(12, 2)) as unit_price
from {{ source('stage', 'transactions') }}
