-- After loading a batch, each Stage transaction ID must be present in Fact exactly once.
select t.transaction_id
from {{ ref('stg_transactions') }} t
left join {{ ref('fact_sales_enriched') }} f on t.transaction_id = f.transaction_id
where f.transaction_id is null
