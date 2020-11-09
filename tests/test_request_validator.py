from app.exception import BadRequest
from app import request_validator as validator
from app.properties import Properties
from app import exception_handler
import pytest


'''
    Given valid headers.
    When a validation is needed.
    Then return 1.
'''
def test_header_validation(mocker):
    mock_header_properties(mocker)

    mocker.patch('app.exception.request')
    request = {'accept':'application/json', 'content-type':'application/json', 'uuid':'uuid'}

    response = validator.validate_header(request)
    assert response == 1

'''
    Given valid headers.
    When a validation is needed.
    Then return 1.
'''
def test_all_header_validation(mocker):
    mock_header_properties(mocker)

    mocker.patch('app.exception.request')
    request = {'accept':'application/json', 'content-type':'application/json', 'uuid':'uuid', 'content-language': 'es'}

    response = validator.validate_header(request)
    assert response == 1

'''
    Given an empty accept header.
    When a validation is needed.
    Then raises a BadRequest exception.
'''
def test_empty_accept_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)
        
        mocker.patch('app.exception.request')
        request = {'accept':'', 'content-type':'application/json'}

        validator.validate_header(request)

'''
    Given an empty content-language header.
    When a validation is needed.
    Then raises a BadRequest exception.
'''
def test_empty_content_language_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)
        
        mocker.patch('app.exception.request')
        request = {'accept':'', 'content-type':'application/json', 'content-language':''}

        validator.validate_header(request)

'''
    Given an invalid content-language header.
    When a validation is needed.
    Then raises a BadRequest exception.
'''
def test_invalid_content_language_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)
        
        mocker.patch('app.exception.request')
        request = {'accept':'', 'content-type':'application/json', 'content-language':'DE'}

        validator.validate_header(request)


def test_empty_uuid_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)

        mocker.patch('app.exception.request')
        request = {'accept':'application/json', 'content-type':'application/json', 'uuid':''}
        
        validator.validate_header(request)

'''
    Given an empty content-type header.
    When a validation is needed.
    Then raises a BadRequest exception.
'''
def test_empty_content_type_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)

        mocker.patch('app.exception.request')
        request = {'accept':'application/json', 'content-type':''}

        validator.validate_header(request)

'''
    Given an invalid accept header.
    When a validation is needed.
    Then raises a BadRequest exception.
'''
def test_mime_type_accept_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)

        mocker.patch('app.exception.request')
        request = {'accept':'text/html', 'content-type':'application/json'}
        validator.validate_header(request)

'''
    Given an invalid content-type header.
    When a validation is needed.
    Then raises a BadRequest exception.
'''
def test_mime_type_content_type_header(mocker):
    with pytest.raises(BadRequest):
        mock_header_properties(mocker)
        
        mocker.patch('app.exception.request')
        request = {'accept':'application/json', 'content-type':'text/html'}

        validator.validate_header(request)

def mock_header_properties(mocker):
    mocker.patch.object(Properties, 'UUID', 'uuid')
    properties = mocker.patch.object(validator, "properties")
    properties_exc = mocker.patch.object(validator, "properties_exc")
    properties.ACCEPT = "accept"
    properties_exc.EXC_ACCEPT_EMPTY_DETAILS = "Details"
    properties_exc.EXC_ACCEPT_EMPTY_LOCATION = "Location"
    properties_exc.EXC_UUID_EMPTY_DETAILS = "Details"
    properties_exc.EXC_UUID_EMPTY_LOCATION = "Location"
    properties_exc.EXC_CONTENT_EMPTY_DETAILS = "Details"
    properties_exc.EXC_CONTENT_EMPTY_LOCATION = "Location"
    properties.CONTENT = "content-type"
    properties.UUID = "uuid"
    properties.REQUEST_FORMAT = "application/json"
    properties.SUCCESS = 1