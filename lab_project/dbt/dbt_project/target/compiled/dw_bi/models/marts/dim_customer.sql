

select distinct
    customer_id,
    concat('Customer ', customer_id) as customer_name
from "warehouse"."dds"."stg_transactions"
where customer_id is not null