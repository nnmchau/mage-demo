if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def test_loader(*args, **kwargs):
    print("START", flush=True)
    return [1, 2, 3]