import subprocess

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

@custom
def run_customer_snapshot_t04(*args, **kwargs):
    """Must run AFTER stage.customers FULL load; BEFORE dbt fact/models."""
    cmd = [
    'dbt', 'snapshot',
    '--select', 'customers_snapshot',
    '--profiles-dir', '/home/src/lab_project/dbt/dbt_project'
    ]
    subprocess.run(cmd, cwd='/home/src/lab_project/dbt/dbt_project', check=True)
    return {'customer_snapshot': 'success'}
