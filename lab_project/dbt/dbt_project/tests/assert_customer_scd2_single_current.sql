-- Every customer has precisely one current version.
select customer_id
from {{ ref('dim_customer_history') }}
group by customer_id
having count(*) filter (where is_current) <> 1
