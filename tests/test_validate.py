import pandas as pd
import pytest
from src.weather_pipeline.validate import validate_frame

def valid_frame():
    return pd.DataFrame([{
        "city": "Jakarta", "observed_at": pd.Timestamp("2026-09-17T00:00:00Z"),
        "temperature_c": 29.0, "relative_humidity_pct": 80.0,
        "precipitation_mm": 0.0, "weather_code": 3,
        "wind_speed_kmh": 9.0, "run_id": "20260917T000000Z",
    }])

def test_valid_frame_passes():
    validate_frame(valid_frame())

def test_invalid_humidity_fails():
    df = valid_frame()
    df.loc[0, "relative_humidity_pct"] = 110
    with pytest.raises(ValueError, match="humidity"):
        validate_frame(df)