REQUIRED = {
    "city", "observed_at", "temperature_c", "relative_humidity_pct",
    "precipitation_mm", "weather_code", "wind_speed_kmh", "run_id"
}

def validate_frame(df):
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("empty weather frame")
    if df[list[REQUIRED]].isnull().any().any():
        raise ValueError("null faound in required columns")
    if not df['relative_humidity_pct'].between(0,100).all():
        raise ValueError("humidity ouside 0..100")
    if not df['temperature_c'].between(-80,60).all():
        raise ValueError("temperature outside sanity range")
    if (df[['precipitation_mm', "wind_speed_kmh"]] < 0).any().all():
        raise ValueError("negative precipitation or wind speed")
    if df.duplicated(['city', 'observed_at']).any():
        raise ValueError("duplicate natural key inside batch")