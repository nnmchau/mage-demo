"""Optional replacement for Tut02 'load_stage' Data Exporter.

Use when the current exporter does if_exists='replace' (DROP/CREATE table).
Keeping the table OID stable is required once dbt staging views exist.
"""
from os import path
from decimal import Decimal
import pandas as pd
from pandas import DataFrame
from psycopg2.extras import execute_values
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def load_stage_safe_t04(df: DataFrame, *args, **kwargs):
    columns = [
        'transaction_id', 'transaction_ts', 'source_updated_at',
        'customer_id', 'product_id', 'quantity', 'unit_price',
    ]
    if df is None or df.empty:
        # Do not leave a stale Stage batch, and do not commit watermark.
        raise ValueError('Empty transaction extraction; demo stops without overwriting Stage')
    if any(col not in df.columns for col in columns):
        raise ValueError(f'Expected columns: {columns}')
    if df['transaction_id'].isna().any() or df['transaction_id'].duplicated().any():
        raise ValueError('transaction_id must be unique and non-null within batch')

    frame = df.copy()
    frame['transaction_ts'] = pd.to_datetime(frame['transaction_ts'], errors='raise')
    frame['source_updated_at'] = pd.to_datetime(frame['source_updated_at'], errors='raise')
    frame['quantity'] = pd.to_numeric(frame['quantity'], errors='raise').astype(int)
    frame['unit_price'] = pd.to_numeric(frame['unit_price'], errors='raise')

    records = []
    for row in frame[columns].itertuples(index=False, name=None):
        tid, ts, upd, cid, pid, qty, price = row
        records.append((str(tid), ts.to_pydatetime(), upd.to_pydatetime(),
                        str(cid), str(pid), int(qty), Decimal(str(price))))

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as pg:
        try:
            with pg.conn.cursor() as cur:
                cur.execute('CREATE SCHEMA IF NOT EXISTS stage')
                cur.execute('''CREATE TABLE IF NOT EXISTS stage.transactions (
                    transaction_id text,
                    transaction_ts timestamp,
                    source_updated_at timestamp,
                    customer_id text,
                    product_id text,
                    quantity integer,
                    unit_price numeric(12,2)
                )''')
                # Delete+insert in same transaction. Do NOT drop/recreate Stage table.
                cur.execute('DELETE FROM stage.transactions')
                execute_values(cur, '''INSERT INTO stage.transactions
                    (transaction_id, transaction_ts, source_updated_at,
                     customer_id, product_id, quantity, unit_price)
                    VALUES %s''', records)
            pg.conn.commit()
        except Exception:
            pg.conn.rollback()
            raise
    print(f'Loaded {len(records)} transactions to Stage (stable table, current batch)')
    return frame
