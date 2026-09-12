CREATE SCHEMA IF NOT EXISTS stage;

CREATE TABLE IF NOT EXISTS stage.transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    transaction_ts TIMESTAMP NOT NULL,

    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,

    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,

    source_file VARCHAR(100),

    loaded_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
);