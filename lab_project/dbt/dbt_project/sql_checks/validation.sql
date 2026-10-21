-- Run these queries in PostgreSQL (e.g., VS Code SQL client).
-- 1. Before dbt: stage data volume and duplicate check.
select count(*) as stage_rows from stage.transactions;

select transaction_id, count(*) as n
from stage.transactions
group by transaction_id
having count(*) > 1;

-- 2. After dbt: dimensions and fact.
select count(*) as customer_count from dds.dim_customer;
select count(*) as product_count from dds.dim_product;

select count(*) as fact_rows,
       coalesce(sum(sales_amount), 0) as total_sales
from dds.fact_sales;

-- 3. Aggregation for BI.
select date_trunc('month', f.sale_date)::date as sale_month,
       p.product_name,
       count(*) as transaction_count,
       sum(f.sales_amount) as total_sales
from dds.fact_sales f
join dds.dim_product p on f.product_id = p.product_id
group by 1, 2
order by 1, 2;
