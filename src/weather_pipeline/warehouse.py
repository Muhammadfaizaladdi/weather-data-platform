import hashlib
from google.api_core.exceptions import Conflict
from google.cloud import bigquery

def load_raw(project_id, dataset_id, table_id, gcs_uri):
    client = bigquery.Client(project=project_id)
    table = f"{project_id}.{dataset_id}.{table_id}"
    # suffix = hashlib.sha256(run_id.encode()).hexdigest()[:20]
    # job_id = f"weather_raw_{suffix}"
    config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=False
    )

    try:
        job = client.load_table_from_uri(gcs_uri, table, job_config=config)
    except Exception as e:
        print(e)
    job.result()
    return job.job_id, job.output_rows or 0