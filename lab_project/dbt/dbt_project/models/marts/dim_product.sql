{{
    config(
        schema='dds',
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key='product_id'
    )
}}

select distinct
    product_id,
    concat('Product ', product_id) as product_name
from {{ ref('stg_transactions') }}
where product_id is not null
