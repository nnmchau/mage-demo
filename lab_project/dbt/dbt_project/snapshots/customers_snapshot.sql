{% snapshot customers_snapshot %}
{{
    config(
        target_schema='history',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='customer_updated_at',
        invalidate_hard_deletes=False
    )
}}
select customer_id, customer_name, city, region, customer_updated_at
from {{ source('stage_dimensions', 'customers') }}
{% endsnapshot %}
