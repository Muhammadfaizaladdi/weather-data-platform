CREATE TABLE IF NOT EXISTS pipeline_runs(
    run_id TEXT PRIMARY KEY,
    logical_date TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    record_count INTEGER,
    raw_uri TEXT,
    bq_job_id TEXT,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS pipeline_watermarks (
    pipeline_name TEXT PRIMARY kEY,
    last_success_at TIMESTAMPTZ NOT NULL,
    update_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

