from os import path
from pandas import DataFrame
from psycopg2.extras import execute_values
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_customers_full(df: DataFrame, *args, **kwargs):
    """Replace FULL current customer snapshot atomically; preserve table metadata."""
    if df is None or df.empty:
        raise ValueError('Refusing empty customer FULL snapshot')
    cols = ['customer_id', 'customer_name', 'city', 'region', 'customer_updated_at']
    records = [tuple(row) for row in df[cols].itertuples(index=False, name=None)]
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as pg:
        try:
            with pg.conn.cursor() as cur:
                cur.execute('CREATE SCHEMA IF NOT EXISTS stage')
                cur.execute("""CREATE TABLE IF NOT EXISTS stage.customers (
                    customer_id text PRIMARY KEY,
                    customer_name text NOT NULL,
                    city text NOT NULL,
                    region text NOT NULL,
                    customer_updated_at timestamp NOT NULL
                )""")
                # DELETE rather than TRUNCATE is safe for dependent views; no DROP/REPLACE.
                cur.execute('ALTER TABLE stage.customers ADD COLUMN IF NOT EXISTS customer_updated_at timestamp')
                cur.execute('DELETE FROM stage.customers')
                execute_values(cur, """INSERT INTO stage.customers
                    (customer_id, customer_name, city, region, customer_updated_at)
                    VALUES %s""", records)
            pg.conn.commit()
        except Exception:
            pg.conn.rollback()
            raise
    print(f'Loaded {len(df)} customer rows (FULL snapshot)')
    return df
