
  
    

  create  table "warehouse"."dds"."dim_customer_history__dbt_tmp"
  
  
    as
  
  (
    
select
    dbt_scd_id as customer_version_key,
    customer_id,
    customer_name,
    city,
    region,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
    (dbt_valid_to is null) as is_current
from "warehouse"."history"."customers_snapshot"
  );
  