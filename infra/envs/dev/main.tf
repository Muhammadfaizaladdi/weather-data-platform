resource "google_project_service" "apis" {
    for_each = toset([
        "storage.googleapis.com",
        "bigquery.googleapis.com",
        "iam.googleapis.com"
    ])
    service = each.value
    disable_on_destroy = false
}

resource "google_storage_bucket" "raw" {
    name = var.raw_bucket
    location = var.region
    uniform_bucket_level_access = true
    force_destroy = false

    versioning { enabled = true }

    lifecycle_rule {
        condition { age = 90 }
        action {
            type = "SetStorageClass"
            storage_class = "NEARLINE"
        }
    }
}

locals {
    datasets=toset([
        "weather_raw", "weather_staging", "weather_intermediate", "weather_analytics"
    ])
}

resource "google_bigquery_dataset" "datasets" {
    for_each = local.datasets
    dataset_id = each.value
    location = var.bq_location
    delete_contents_on_destroy = false
}

resource "google_service_account" "pipeline" {
    account_id = "weather-local-pipeline"
    display_name = "Weather local pipeline"
}

resource "google_project_iam_member" "pipeline_bq_job_user" {
    project=var.project_id
    role= "roles/bigquery.jobUser"
    member="serviceAccount:${google_service_account.pipeline.email}"
}

resource "google_project_iam_member" "pipeline_bq_editor" {
    project=var.project_id
    role= "roles/bigquery.dataEditor"
    member="serviceAccount:${google_service_account.pipeline.email}"
}

resource "google_storage_bucket_iam_member" "pipeline_object_user" {
    bucket=google_storage_bucket.raw.name
    role= "roles/storage.objectUser"
    member="serviceAccount:${google_service_account.pipeline.email}"
}


resource "google_bigquery_table" "weather_hourly_raw" {
    dataset_id = google_bigquery_dataset.datasets["weather_raw"].dataset_id
    table_id = "weather_hourly"
    deletion_protection = true

    time_partitioning {
        type = "DAY"
        field = "observed_at"
    }
    clustering = ["city","source"]
    require_partition_filter = true

    schema = jsonencode([
        { name="ingestion_id", type="STRING", mode="REQUIRED" },
        { name="run_id", type="STRING", mode="REQUIRED" },
        { name="city", type="STRING", mode="REQUIRED" },
        { name="latitude", type="FLOAT", mode="REQUIRED" },
        { name="longitude", type="FLOAT", mode="REQUIRED" },
        { name="observed_at", type="TIMESTAMP", mode="REQUIRED" },
        { name="local_time", type="DATETIME", mode="REQUIRED" },
        { name="temperature_c", type="FLOAT", mode="REQUIRED" },
        { name="relative_humidity_pct", type="FLOAT", mode="REQUIRED" },
        { name="weather_code", type="INTEGER", mode="REQUIRED" },
        { name="wind_speed_kmh", type="FLOAT", mode="REQUIRED" },
        { name="source", type="STRING", mode="REQUIRED" },
        { name="ingested_at", type="TIMESTAMP", mode="REQUIRED" }
    ])
}


output "pipeline_service_account"  {value = google_service_account.pipeline.email}
output "raw_bucket" {value=google_storage_bucket.raw.name}