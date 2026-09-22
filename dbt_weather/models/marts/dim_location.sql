select distinct
    {{ dbt_utils.generate_surrogate_key(['city']) as location_key }},
    city,
    latitude,
    longitude
from {{ ref('stg_weather_hourly') }}