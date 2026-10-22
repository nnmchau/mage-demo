
  
    

  create  table "warehouse"."dds"."dim_product_scd1__dbt_tmp"
  
  
    as
  
  (
    
select product_id as product_key, product_id, product_name, subcategory, category
from "warehouse"."dds"."stg_products"
  );
  