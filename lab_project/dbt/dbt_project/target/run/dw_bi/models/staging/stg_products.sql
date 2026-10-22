
  create view "warehouse"."dds"."stg_products__dbt_tmp"
    
    
  as (
    
select
    trim(product_id::text) as product_id,
    trim(product_name::text) as product_name,
    trim(subcategory::text) as subcategory,
    trim(category::text) as category
from "warehouse"."stage"."products"
  );