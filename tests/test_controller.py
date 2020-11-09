import pytest
from app import emailfunction, request_validator
from app import controller
from app.exception import BadRequest

'''
    Given valid request.
    When send function is called.
    Then return a response with the properties values.
'''
def test_send_true(mocker):
    request = mocker.patch.object(controller, 'request')
    mocker.patch('app.request_validator.validate_header', return_value = True)
    mocker.patch('app.request_validator.validate_request_body', return_value=True)
    mocker.patch('app.emailfunction.send', return_value=True)
    request.json = {"subject": "This is a valid test", "body": "Congrats! your file is validated", "mail_list" : ["test@citi.com"], "issuer_mail" : "test@citi.com"}
    response = controller.send()

    assert response.status == '200 OK'
