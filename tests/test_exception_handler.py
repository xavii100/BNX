from app.exception_handler import GlobalExceptionHandler
from app import exception_handler as exc
from app.properties import Properties
from app.exception import BadRequest
from http import HTTPStatus as http
import pytest

'''
    Given an Forbidden exception and a request.
    When an Forbidden exception is raised.
    Then return a response with status = '403 FORBIDDEN'.
'''
def test_forbidden(mocker):
    request = mocker.patch('app.exception_handler.request')
    exception = mocker.patch('werkzeug.exceptions.Forbidden')
    properties = mocker.patch.object(exc, 'prop_exc')

    formatResponse = mocker.patch.object(exc, 'prop')
    formatResponse.REQUEST_FORMAT = 'application/json'
    dict_uuid = {
        'uuid': 'uuid'
    }

    request.headers = dict_uuid    
    properties.EXC_FORBIDDEN_DETAILS = 'Details'
    properties.EXC_FORBIDDEN_LOCATION = 'Location'
    
    response = GlobalExceptionHandler.handle_forbidden(exception)
    assert response.status == '403'

'''
    Given a NotFound exception and a request.
    When a NotFound exception is raised.
    Then return a response with status = '404 NOT FOUND'.
'''
def test_not_found(mocker):
    request = mocker.patch('app.exception_handler.request')
    exception = mocker.patch('werkzeug.exceptions.NotFound')
    properties = mocker.patch.object(exc, 'prop_exc')

    formatResponse = mocker.patch.object(exc, 'prop')
    formatResponse.REQUEST_FORMAT = 'application/json'
    dict_uuid = {
        'uuid': 'uuid'
    }

    request.headers = dict_uuid
    properties.EXC_NOT_FOUND_DETAILS = 'Details'
    properties.EXC_NOT_FOUND_LOCATION = 'Location'
    
    response = GlobalExceptionHandler.handle_not_found(exception)
    assert response.status == '404'

'''
    Given a MethodNotAllowed exception and a request.
    When a MethodNotAllowed exception is raised.
    Then return a response with status = '405 METHOD NOT ALLOWED'.
'''
def test_method_not_allowed(mocker):
    request = mocker.patch('app.exception_handler.request')
    exception = mocker.patch('werkzeug.exceptions.MethodNotAllowed')
    properties = mocker.patch.object(exc, 'prop_exc')
    
    formatResponse = mocker.patch.object(exc, 'prop')
    formatResponse.REQUEST_FORMAT = 'application/json'
    dict_uuid = {
        'uuid': 'uuid'
    }

    request.headers = dict_uuid    
    properties.EXC_METHOD_NOT_ALLOWED_DETAILS = 'Details'
    properties.EXC_METHOD_NOT_ALLOWED_LOCATION = 'Location'
    
    response = GlobalExceptionHandler.handle_method_not_allowed(exception)
    assert response.status == '404'

'''
    Given a BadRequest exception and a request.
    When a BadRequest exception is raised.
    Then return a response with status = '400 BAD REQUEST'.
'''
def test_bad_request_exception(mocker):
    request = mocker.patch('app.exception_handler.request')
    formatResponse = mocker.patch.object(exc, 'prop')
    formatResponse.REQUEST_FORMAT = 'application/json'

    exception = mocker.patch('werkzeug.exceptions.BadRequest')
    properties = mocker.patch.object(exc, 'prop_exc')
    dict_uuid = {
        'uuid': 'uuid'
    }

    request.headers = dict_uuid
    properties.EXC_BAD_REQUEST_DETAILS = 'Details'
    properties.EXC_BAD_REQUEST_LOCATION = 'Location'

    response = GlobalExceptionHandler.handle_bad_request(exception)
    assert response.status == '400'
    