

select
    t.transaction_id,
    t.transaction_ts,
    cast(t.transaction_ts as date) as sale_date,
    t.source_updated_at,
    c.customer_id,
    p.product_id,
    t.quantity,
    t.unit_price,
    cast(t.quantity * t.unit_price as numeric(14, 2))
        as sales_amount
from "warehouse"."dds"."stg_transactions" t
left join "warehouse"."dds"."dim_customer" c
    on t.customer_id = c.customer_id
left join "warehouse"."dds"."dim_product" p
    on t.product_id = p.product_id