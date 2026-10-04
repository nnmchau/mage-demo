import pandas as pd
from mage_ai.io.file import FileIO

from pathlib import Path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    For multiple directories, use the following:
        FileIO().load(file_directories=['dir_1', 'dir_2'])

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    source_folder = kwargs.get(
        'source_folder',
        '/home/src/data/landing'
    )

    file_pattern = kwargs.get(
        'file_pattern',
        'transactions_*.csv'
    )

    files = list(
        Path(source_folder).glob(file_pattern)
    )

    print(f'Files found: {len(files)}')

    dataframes = []

    for file in files:

        df = pd.read_csv(file)

        df['source_file'] = file.name

        dataframes.append(df)

    if not dataframes:
        return pd.DataFrame()

    df = pd.concat(
        dataframes,
        ignore_index=True
    )

    print(f'Rows read: {len(df)}')

    return df