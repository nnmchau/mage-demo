CREATE SCHEMA IF NOT EXISTS stage;
CREATE SCHEMA IF NOT EXISTS dds;
CREATE SCHEMA IF NOT EXISTS control;

CREATE TABLE IF NOT EXISTS stage.transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    transaction_ts TIMESTAMP NOT NULL,
    source_updated_at TIMESTAMP NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    source_file VARCHAR(200),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS control.etl_watermark (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_successful_extraction_time TIMESTAMP NOT NULL
);

INSERT INTO control.etl_watermark (
    pipeline_name,
    last_successful_extraction_time
)
VALUES (
    'transaction_ingestion',
    '1900-01-01 00:00:00'
)
ON CONFLICT (pipeline_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS control.processed_transaction (
    transaction_id VARCHAR(20) PRIMARY KEY,
    first_processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

