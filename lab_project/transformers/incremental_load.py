import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(extraction_window, data , *args, **kwargs):
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
    print(type(data))
    print(type(extraction_window))

    if data.empty:
        return data

    df = data.copy()

    lset = pd.Timestamp(extraction_window['lset'])
    cet = pd.Timestamp(extraction_window['cet'])
    df['source_updated_at'] = pd.to_datetime(df['source_updated_at'])

    filtered = pd.DataFrame(columns=df.columns)

    filtered = df[
        (df['source_updated_at'] > lset)
        &
        (df['source_updated_at']<= cet)
    ].copy()

    print(f'LSET: {lset}')
    print(f'CET: {cet}')

    return filtered

