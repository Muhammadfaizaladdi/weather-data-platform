{{
    config(
        materialized='incremental',
        unique_key=['city', 'observed_at'],
        incremental_strategy
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['city', 'observed_at']) }} as weather_key,
    city,
    observed_at,
    temperatur_c,
    relative_humidity_pct,
    precipitation_mm,
    weather_code,
    wind_speed_kmh,
    run_id,
    ingested_at
from {{ ref('stg_weather_hourly') }}
{% if is_incremental() %}
where observed_at >= timestamp_sub(
    ( select coalesce(max(observed_at), timestamp('1970-01-01')) from {{ this }} ),
    interval 2 day
)
{% endif %}