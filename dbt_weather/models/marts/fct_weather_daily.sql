select
  city,
  date(observed_at) as weather_date,
  min(temperature_c) as min_temperature_c,
  max(temperature_c) as max_temperature_c,
  avg(temperature_c) as avg_temperature_c,
  sum(precipitation_mm) as total_precipitation_mm,
  max(wind_speed_kmh) as max_wind_speed_kmh
from {{ ref('fct_weather_hourly') }}
group by 1, 2