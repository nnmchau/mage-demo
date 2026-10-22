{{
    config(
        schema='dds',
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key='transaction_id'
    )
}}
-- Grain: exactly one row per transaction_id.
-- Stage holds current batch only; rerunning the same batch replaces matching IDs.
select
    t.transaction_id,
    t.transaction_ts,
    cast(t.transaction_ts as date) as sale_date,
    d.date_key,
    t.source_updated_at,
    c.customer_version_key, -- FK to the specific SCD2 customer version
    c.customer_id,
    p.product_key,          -- SCD1 key is stable natural product_id
    p.product_id,
    t.quantity,
    t.unit_price,
    cast(t.quantity * t.unit_price as numeric(14, 2)) as sales_amount
from {{ ref('stg_transactions') }} t
left join {{ ref('dim_date') }} d
    on cast(t.transaction_ts as date) = d.full_date
left join {{ ref('dim_product_scd1') }} p
    on t.product_id = p.product_id
left join {{ ref('dim_customer_history') }} c
    on t.customer_id = c.customer_id
   and t.transaction_ts >= c.valid_from
   and (t.transaction_ts < c.valid_to or c.valid_to is null)
