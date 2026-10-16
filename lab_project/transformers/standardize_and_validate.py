import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    if data.empty:
        return data

    df = data.copy()

    # Standardize string fields
    for column in [ 'transaction_id', 'customer_id','product_id',]:
        df[column] = (
            df[column]
            .astype('string')
            .str.strip()
        )

     # Standardize data types

    df['transaction_ts'] = pd.to_datetime(df['transaction_ts'], errors='coerce')
    df['source_updated_at'] = pd.to_datetime(df['source_updated_at'], errors='coerce')


    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # Basic validation -  remove rows with null values
    rows_before = len(df)
    df = df[
        df['transaction_id'].notna()
        &
        df['customer_id'].notna()
        &
        df['product_id'].notna()
        &
        df['transaction_ts'].notna()
        &
        df['source_updated_at'].notna()
        &
        (df['quantity'] > 0)
        &
        (df['unit_price'] >= 0)
    ]

    print(
        f'Invalid rows removed: '
        f'{rows_before - len(df)}'
    )

    return df
