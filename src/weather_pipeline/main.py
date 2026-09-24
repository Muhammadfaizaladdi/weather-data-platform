import argparse
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import pandas as pd
from .config import CITIES
from .extract import fetch_weather
from .transform import normalize
from .validate import validate_frame
from .storage import upload_ndjson
from .warehouse import load_raw
from .metadata import mark_failed, mark_started, mark_success

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

def run(logical_date: str, run_id: str):
    mark_started(run_id, logical_date=logical_date)
    try:
        frames = []
        for city, (lat, lon, tz) in CITIES.items():
            payload = fetch_weather(city, lat, lon, tz)
            normalized_data = normalize(city, lat, lon, tz, payload, run_id)
            frames.append(normalized_data)
        frame = pd.concat(frames, ignore_index=True)
        validate_frame(frame)
        object_name = f"raw/weather/logical_date={logical_date}/run_id={run_id}/weather.ndjson"
        
        print(os.environ['RAW_BUCKET'])
        uri = upload_ndjson(frame, os.environ['RAW_BUCKET'], object_name)
        job_id, rows = load_raw(os.environ['PROJECT_ID'], os.environ["BQ_RAW_DATASET"], 'weather_hourly', uri)
        mark_success(run_id, rows, uri, job_id)
        print("hmm2")
    except Exception as e:
        mark_failed(run_id, repr(e))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--logical-date', required=True)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    run(args.logical_date, args.run_id)
