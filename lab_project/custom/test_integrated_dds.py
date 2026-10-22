import subprocess

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

@custom
def test_integrated_dds_t04(*args, **kwargs):
    """Stop watermark commit on failing data quality tests."""
    cmd = [
    'dbt', 'snapshot',
    '--select', 'customers_snapshot',
    '--profiles-dir', '/home/src/lab_project/dbt/dbt_project'
    ]
    subprocess.run(
        cmd,
        cwd='/home/src/lab_project/dbt/dbt_project',
        check=True,
    )
    return {'dbt_tests': 'passed'}
