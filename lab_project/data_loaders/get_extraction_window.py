import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    pipeline_name = kwargs.get(
        'pipeline_name',
        'transaction_ingestion'
    )

    query = f"""
            SELECT last_successful_extraction_time
            FROM control.etl_watermark
            WHERE pipeline_name = '{pipeline_name}'
            """  # Specify your SQL query here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        watermark = loader.load(query)

    lset = pd.Timestamp(
        watermark.iloc[0][
            'last_successful_extraction_time'
        ]
    )

    cet_override = kwargs.get('cet_override')

    if cet_override:
        cet = pd.Timestamp(cet_override)
    else:
        cet = pd.Timestamp.now()

    print (lset)
    print(cet)

    return {
        'lset': lset,
        'cet': cet,
    }

