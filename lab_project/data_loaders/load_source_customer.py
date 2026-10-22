from pathlib import Path
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_customers_full(*args, **kwargs):
    name = kwargs.get('customer_file', 'customers_full_v1.csv')
    print('get name done')
    if name not in {'customers_full_v1.csv', 'customers_full_v2.csv'}:
        raise ValueError('customer_file must be customers_full_v1.csv or customers_full_v2.csv')
    path = Path('/home/src/data/source/dimensions') / name
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    print('read file: done')
    cols = ['customer_id', 'customer_name', 'city', 'region', 'customer_updated_at']
    if not all(col in df.columns for col in cols):
        raise ValueError(f'Missing customer columns; required={cols}')
    df = df[cols].copy()
    print('check cols: done')
    for c in cols:
        df[c] = df[c].str.strip()
    if df.empty or df[cols].eq('').any().any() or df.customer_id.duplicated().any():
        raise ValueError('Customer full snapshot must be non-empty, complete and unique')
    df['customer_updated_at'] = pd.to_datetime(df['customer_updated_at'], errors='raise')
    print('finish and return')
    return df
