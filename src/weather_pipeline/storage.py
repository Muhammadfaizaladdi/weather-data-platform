import json
from google.api_core.exceptions import PreconditionFailed
from google.cloud import storage

def to_jsonable(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value

def upload_ndjson(df, bucket_name, object_name):
    print(df.head())

    body = "\n".join(
        json.dumps({k: to_jsonable(v) for k, v in row.items()}, default=str) 
        for row in df.to_dict(orient="records")
    ) + "\n"

    print(body)

    blob = storage.Client().bucket(bucket_name).blob(object_name)
    try:
        blob.upload_from_string(
            body, content_type="application/x-ndjson", if_generation_match=0
        )
    except PreconditionFailed:
        pass
    return f"gs://{bucket_name}/{object_name}"

