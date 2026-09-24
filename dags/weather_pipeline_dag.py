from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data-team-112233',
    'retries': 3,
    'retry_delay': timedelta(minutes=(5)),
    "execution_timeout": timedelta(minutes=30)
}

with DAG(
    dag_id = 'weather_intelligence_hourly',
    start_date = datetime(2026, 9, 15),
    schedule = "0 * * * *",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=['weather', 'batch', 'hybrid']
) as dag:
    ingest = BashOperator(
        task_id = 'ingest_weather',
        bash_command = (
            "cd /opt/airflow/project && "
            "python -m src.weather_pipeline.main "
            "--logical-date '{{ data_interval_start.isoformat() }}' "
            "--run-id '{{ run_id }}'"
        ),
    )

    dbt_build = BashOperator(
        task_id = "dbt_build",
        bash_command = (
            "cd /opt/airflow/project/dbt_weahter && "
            "dbt deps && dbt build --select +fct_weahter_daily"
        )
    )

    quality_check = BashOperator(
        task_id="quality_check",
        bash_command=(
            "bq query --use_legacy_sql=false --format=none "
            "'ASSERT (SELECT COUNT(*) FROM `{{ var.value.project_id }}.weather_analytics.fct_weather_hourly` "
            "WHERE observed_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)) > 0 "
            "AS \"No recent weather rows\"'"
        ),
    )

    ingest >> dbt_build >> quality_check