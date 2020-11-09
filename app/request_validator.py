from app.exception import BadRequest
from app.log import log
from app.properties_exc import PropertiesException
from app.properties import Properties
from app.properties_log import PropertiesLog
from app import validation_request
import re

is_empty = lambda header: not header
is_not_string = lambda path: type(path) != str
mime_type = lambda header: header != 'application/json'


properties = Properties()
properties_exc = PropertiesException()

'''
    Function to validate headers of the request.
'''
def validate_header(request):
    log.info('Validating headers')

    __not_empty(request.get(properties.ACCEPT), 
                        properties_exc.EXC_ACCEPT_EMPTY_DETAILS,
                        properties_exc.EXC_ACCEPT_EMPTY_LOCATION)
    __validate_mime_type(request.get(properties.ACCEPT), 
                        properties_exc.EXC_ACCEPT_TYPE_DETAILS, 
                        properties_exc.EXC_ACCEPT_TYPE_LOCATION)
    
    __not_empty(request.get(properties.UUID),
                        properties_exc.EXC_UUID_EMPTY_DETAILS,
                        properties_exc.EXC_UUID_EMPTY_LOCATION)

    __not_empty(request.get(properties.CONTENT), 
                        properties_exc.EXC_CONTENT_EMPTY_DETAILS,
                        properties_exc.EXC_CONTENT_EMPTY_LOCATION)
    __validate_mime_type(request.get(properties.CONTENT), 
                        properties_exc.EXC_CONTENT_TYPE_DETAILS, 
                        properties_exc.EXC_CONTENT_TYPE_LOCATION)

    return properties.SUCCESS

'''
    Function to validate the request body.
'''
def validate_request_body(request):
    log.info('Validating request body')

    __is_invalid_request(request)

    __validate(is_empty(request.get("issuer_mail")), "issuer_mail cannot be null nor empty", "issuer_mail")
    if validation_request.is_invalid_email(request.get("issuer_mail")):   
        log.info('%s, %s', "Invalid issuer_mail format", "issuer_mail")
        raise BadRequest("Invalid issuer_mail format", "issuer_mail")  

    __validate(is_empty(request.get("mail_list")), "mail_list cannot be null nor empty", "mail_list")
    if validation_request.is_invalid_any_email(request.get("mail_list")):     
        log.info('%s, %s', "Invalid email format", "mail_list")
        raise BadRequest("Invalid email format", "mail_list") 
    
    __validate(is_empty(request.get("subject")), "subject cannot be null nor empty", "subject")

    __validate(is_empty(request.get("body")), "body cannot be null nor empty", "body")

    return properties.SUCCESS

def __validate(invalid, details, location):
    if invalid: 
        log.error(details, location)
        raise BadRequest(details, location) 

'''
    Function to validate that a path is a string.
'''
def __is_string(string_value, details, location):
    if type(string_value) != str:
        log.info('%s, %s', details, string_value)
        raise BadRequest(details, location)

'''
    Function to validate that a param is not empty.
'''
def __not_empty(param, details, location):
    if not param:
        log.info('%s', details)
        raise BadRequest(details, location)

'''
    Function to validate that a header is equal to "application/json".
'''
def __validate_mime_type(header, details, location):
    if header != properties.REQUEST_FORMAT:
        log.info('%s', details)
        raise BadRequest(details, location)


def __is_invalid_request(request):
    valid_keys = ["mail_list","issuer_mail","subject","body"]
    invalid_keys = list()
    for key in valid_keys:
        if key not in request:
            invalid_keys.append(key)
    if len(invalid_keys) != 0:
        __validate(True,"{0} cannot be null nor empty".format(invalid_keys[0]),invalid_keys[0])