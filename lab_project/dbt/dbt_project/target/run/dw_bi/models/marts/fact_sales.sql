
      
        
            delete from "warehouse"."dds"."fact_sales"
            where (
                transaction_id) in (
                select (transaction_id)
                from "fact_sales__dbt_tmp132018787746"
            );

        
    

    insert into "warehouse"."dds"."fact_sales" ("transaction_id", "transaction_ts", "sale_date", "source_updated_at", "customer_id", "product_id", "quantity", "unit_price", "sales_amount")
    (
        select "transaction_id", "transaction_ts", "sale_date", "source_updated_at", "customer_id", "product_id", "quantity", "unit_price", "sales_amount"
        from "fact_sales__dbt_tmp132018787746"
    )
  