from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY = [
    "temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "wind_speed_10m"
]

def build_session() -> Session:
    retry = Retry(total=4, backoff_factor=1, status_forcelist=[429,500,502,503,504])
    sessions = Session()
    sessions.mount("https://", HTTPAdapter(max_retries=retry))
    return sessions

def fetch_weather(city: str, lat: float, long: float, timezone: str) -> dict:
    params = {
        "latitude": lat,
        "longitude": long,
        "timezone": timezone,
        "hourly": ",".join(HOURLY),
        "forceast_days": 2
    }

    session = build_session()
    try:
        response = session.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except Exception as e:
        print(e)
    if "hourly" not in payload:
        raise ValueError(f"hourly missing for {city}")
    return payload
