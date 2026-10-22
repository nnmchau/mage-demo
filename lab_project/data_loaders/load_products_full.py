from pathlib import Path
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_products_full(*args, **kwargs):
    name = kwargs.get('product_file') or 'products_full_v1.csv'
    allowed = {'products_full_v1.csv', 'products_full_v2.csv'}
    if name not in allowed:
        raise ValueError(f'Invalid product_file: {name}')
    filepath = Path('/home/src/data/source/dimensions') / name
    df = pd.read_csv(filepath, dtype=str).fillna('')
    required = ['product_id', 'product_name', 'subcategory', 'category']
    if not all(c in df.columns for c in required):
        raise ValueError('Missing column(s) in product CSV')
    df = df[required].copy()
    for col in required:
        df[col] = df[col].astype(str).str.strip()
    if df.empty or df['product_id'].eq('').any() or df['product_id'].duplicated().any():
        raise ValueError('Products must be non-empty and product_id unique/not blank')
    print(f'Reading FULL Product snapshot: {name} ({len(df)} rows)')
    return df
