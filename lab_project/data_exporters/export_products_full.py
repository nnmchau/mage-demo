from os import path
from pandas import DataFrame
from psycopg2.extras import execute_values
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_products_full(df: DataFrame, *args, **kwargs):
    if df is None or df.empty:
        raise ValueError('Refusing to overwrite Stage with an empty snapshot')
    cols = ['product_id', 'product_name', 'subcategory', 'category']
    data = [tuple(v) for v in df[cols].itertuples(index=False, name=None)]
    cfg = path.join(get_repo_path(), 'io_config.yaml')
    with Postgres.with_config(ConfigFileLoader(cfg, 'default')) as pg:
        try:
            with pg.conn.cursor() as cur:
                cur.execute('CREATE SCHEMA IF NOT EXISTS stage')
                cur.execute('CREATE TABLE IF NOT EXISTS stage.products (product_id text, product_name text, subcategory text, category text)')
                cur.execute('DELETE FROM stage.products')
                execute_values(cur, 'INSERT INTO stage.products (product_id, product_name, subcategory, category) VALUES %s', data)
            pg.conn.commit()
        except Exception:
            pg.conn.rollback()
            raise
    print(f'Loaded {len(df)} rows into stage.products (full snapshot)')
    return df
