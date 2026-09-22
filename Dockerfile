FROM apache/airflow:2.10.5-python3.11

USER airflow

ENV PIP_TIMEOUT=100
RUN pip install --no-cache-dir \
    apache-airflow-providers-google \
    google-cloud-storage \
    google-cloud-bigquery \
    pandas \
    pyarrow \
    requests \
    psycopg2-binary \
    pydantic \
    sqlalchemy \
    dbt-bigquery \
    pytest