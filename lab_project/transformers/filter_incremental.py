import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(source_df, extraction_window, *args, **kwargs):
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

    if source_df.empty:
        return source_df

    df = source_df.copy()

    # Convert source_updated_at to Timestamps
    df['source_updated_at'] = pd.to_datetime(df['source_updated_at']) 

    # Convert data type of LSET and CET
    lset = pd.Timestamp(extraction_window['lset'])
    cet = pd.Timestamp(extraction_window['cet'])

    filtered = df[
        (df['source_updated_at'] > lset)
        &
        (df['source_updated_at'] <= cet)
    ]

    print(f'LSET: {lset}')
    print(f'CET : {cet}')
    print(
        f'Rows in extraction window: '
        f'{len(filtered)}'
    )

    return filtered