with ranked as(
    select *, row_number() over (
        partition by city, observed_at order by ingested_at desc
    ) as row_num
    from {{ source('weather_raw', 'weather_hourly') }}
)

select 
    city,
    latitude,
    longitude,
    observed_at,
    local_time,
    temperatur_c,
    relative_humidity_pct,
    precipitation_mm,
    weather_code,
    wind_speed_kmh,
    source,
    run_id,
    ingested_at
from ranked where row_num=1