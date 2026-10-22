if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_customers_full(*args, **kwargs):
    print('START LOAD CUSTOMERS', flush=True)

    return {
        'status': 'success',
        'message': 'Data Loader executed'
    }