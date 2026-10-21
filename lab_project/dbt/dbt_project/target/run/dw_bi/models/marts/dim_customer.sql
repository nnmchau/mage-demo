
      
        
            delete from "warehouse"."dds"."dim_customer"
            where (
                customer_id) in (
                select (customer_id)
                from "dim_customer__dbt_tmp132018686600"
            );

        
    

    insert into "warehouse"."dds"."dim_customer" ("customer_id", "customer_name")
    (
        select "customer_id", "customer_name"
        from "dim_customer__dbt_tmp132018686600"
    )
  