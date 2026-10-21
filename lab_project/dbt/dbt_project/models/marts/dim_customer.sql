{{
    config(
        schema='dds',
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key='customer_id'
    )
}}

select distinct
    customer_id,
    concat('Customer ', customer_id) as customer_name
from {{ ref('stg_transactions') }}
where customer_id is not null
