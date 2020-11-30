from app import utils

def test_path_from_list():
    path = 'Test'
    response = utils.get_path_from_list(path)
    assert type(response) == str