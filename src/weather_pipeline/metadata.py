import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

print(os.environ)

def engine():
    # Gunakan .get() untuk handle default value dan hindari bentrok kutip di f-string
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST', 'postgres')
    port = os.environ.get('POSTGRES_PORT', '5432')
    db = os.environ.get('POSTGRES_DB')

    dsn = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    conn = create_engine(dsn, pool_pre_ping=True)
    return conn

def mark_started(run_id, logical_date):
    with engine().begin() as conn:
        sql_s = """
                INSERT INTO pipeline_runs(run_id, logical_date, status)
                VALUES (:run_id, :logical_date, 'RUNNING')
                ON CONFLICT(run_id) DO UPDATE SET status='RUNNING', error_message=NULL
                """
        
        conn.execute(text(sql_s), {"run_id":run_id, "logical_date": logical_date})

def mark_success(run_id, count, uri, job_id):
    with engine().begin() as conn:
        sql_s = """
                UPDATE pipeline_runs SET status='SUCCESS', finished_at=NOW(),
                record_count=:count, raw_uri=:uri, bq_job_id=:job_id WHERE run_id=:run_id
                """
        
        conn.execute(text(sql_s), {"run_id":run_id, "count":count, "uri":uri, "job_id":job_id})

        sql_s = """
                INSERT INTO pipeline_watermarks(pipeline_name, last_success_at)
                SELECT 'weather_hourly', logical_date FROM pipeline_runs WHERE run_id=:run_id
                ON CONFLICT(pipeline_name) DO UPDATE
                SET last_success_at=GREATEST(pipeline_watermarks.last_success_at, EXCLUDED.last_success_at), 
                update_at=NOW()
                """

        conn.execute(text(sql_s), {"run_id":run_id})


def mark_failed(run_id, error):
    sql_s = text("""
        UPDATE pipeline_runs 
        SET status = 'FAILED', finished_at = NOW(), error_message = :error
        WHERE run_id = :run_id
    """)
    with engine().begin() as conn:
        conn.execute(sql_s, {"run_id": run_id, "error": error})

# run_id = "123"
# logical_date = "'2026-09-24T17:00:00+00:00'"
# count = 10
# uri = "https:///"
# job_id = "1234567"
# error = "hahaha"

# mark_started(run_id, logical_date)
# mark_failed(run_id, error)
# mark_success(run_id, count,uri,job_id)