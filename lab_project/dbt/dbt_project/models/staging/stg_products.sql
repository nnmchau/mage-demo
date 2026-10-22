{{ config(schema='dds', materialized='view') }}
select
    trim(product_id::text) as product_id,
    trim(product_name::text) as product_name,
    trim(subcategory::text) as subcategory,
    trim(category::text) as category
from {{ source('stage_dimensions', 'products') }}
