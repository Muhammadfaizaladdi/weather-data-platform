from datetime import datetime, timezone
from uuid import uuid4
from zoneinfo import ZoneInfo
import pandas as pd

def normalize(city, lat, lon, tz_name, payload, run_id):
    frame = None
    hourly = payload['hourly']

    frame = pd.DataFrame({
        "local_time": hourly['time'],
        "temperature_c": hourly['temperature_2m'],
        "relative_humidity_pct": hourly["relative_humidity_2m"],
        "precipitation_mm": hourly["precipitation"],
        "weather_code": hourly["weather_code"],
        "wind_speed_kmh": hourly["wind_speed_10m"]
    })

    local = pd.to_datetime(frame['local_time']).dt.tz_localize(ZoneInfo(tz_name))
    frame['local_time'] = pd.to_datetime(frame['local_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    frame['observed_at'] = local.dt.tz_convert("UTC")
    frame['city'] = city
    frame['latitude'] = lat
    frame['longitude'] = lon
    frame['source'] = "open_meteo"
    frame['run_id'] = run_id
    frame['ingestion_id'] = str(uuid4())
    frame['ingested_at'] = datetime.now(timezone.utc)
    return frame