

select distinct
    product_id,
    concat('Product ', product_id) as product_name
from "warehouse"."dds"."stg_transactions"
where product_id is not null