-- No SCD2 version's validity overlaps another version for same natural key.
select a.customer_id
from {{ ref('dim_customer_history') }} a
join {{ ref('dim_customer_history') }} b
  on a.customer_id = b.customer_id
 and a.customer_version_key < b.customer_version_key
 and a.valid_from < coalesce(b.valid_to, 'infinity'::timestamp)
 and b.valid_from < coalesce(a.valid_to, 'infinity'::timestamp)
limit 1
