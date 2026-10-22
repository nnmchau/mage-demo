
      
        
            delete from "warehouse"."dds"."fact_sales_enriched"
            where (
                transaction_id) in (
                select (transaction_id)
                from "fact_sales_enriched__dbt_tmp100029140356"
            );

        
    

    insert into "warehouse"."dds"."fact_sales_enriched" ("transaction_id", "transaction_ts", "sale_date", "date_key", "source_updated_at", "customer_version_key", "customer_id", "product_key", "product_id", "quantity", "unit_price", "sales_amount")
    (
        select "transaction_id", "transaction_ts", "sale_date", "date_key", "source_updated_at", "customer_version_key", "customer_id", "product_key", "product_id", "quantity", "unit_price", "sales_amount"
        from "fact_sales_enriched__dbt_tmp100029140356"
    )
  