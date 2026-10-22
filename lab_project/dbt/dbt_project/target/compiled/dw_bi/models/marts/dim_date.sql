
with calendar as (
    select gs::date as full_date
    from generate_series(
        '2025-01-01'::date,
        '2027-12-31'::date,
        interval '1 day'
    ) as gs
)
select
    to_char(full_date, 'YYYYMMDD')::integer as date_key,
    full_date,
    extract(year from full_date)::integer as year,
    extract(quarter from full_date)::integer as quarter,
    extract(month from full_date)::integer as month,
    to_char(full_date, 'FMMonth') as month_name,
    extract(day from full_date)::integer as day,
    extract(isodow from full_date)::integer as iso_day_of_week,
    (extract(isodow from full_date) in (6, 7)) as is_weekend,
    to_char(full_date, 'YYYY-MM') as year_month
from calendar