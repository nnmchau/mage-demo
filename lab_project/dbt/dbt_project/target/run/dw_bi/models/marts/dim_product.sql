
      
        
            delete from "warehouse"."dds"."dim_product"
            where (
                product_id) in (
                select (product_id)
                from "dim_product__dbt_tmp132018692035"
            );

        
    

    insert into "warehouse"."dds"."dim_product" ("product_id", "product_name")
    (
        select "product_id", "product_name"
        from "dim_product__dbt_tmp132018692035"
    )
  