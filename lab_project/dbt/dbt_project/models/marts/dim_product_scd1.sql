{{ config(schema='dds', materialized='table') }}
select product_id as product_key, product_id, product_name, subcategory, category
from {{ ref('stg_products') }}
