from app.properties_exc import PropertiesException 
from app.exception import GenericException
from app.response import ErrorResponse
from app.custom_enum import ErrorType 
from app.properties import Properties
from app.properties_log import PropertiesLog
from app.log import log
from werkzeug.exceptions import NotFound, MethodNotAllowed, Forbidden, BadRequest
from flask import Blueprint, Response, request
from http import HTTPStatus as http
from datetime import datetime
from requests import ConnectionError
import json

exception = Blueprint('exeption', __name__)
prop = Properties()
prop_exc = PropertiesException()
properties_log = PropertiesLog()

class GlobalExceptionHandler:

    '''
        Builds an error response from the http 400 status code

        @error as the exception.
    '''
    @exception.app_errorhandler(BadRequest)
    def handle_bad_request(error):
        now = datetime.now()
        return GlobalExceptionHandler.__build_response(ErrorType.INVALID.name, 
                str(http.BAD_REQUEST.value),
                prop_exc.EXC_BAD_REQUEST_DETAILS, 
                prop_exc.EXC_BAD_REQUEST_LOCATION, 
                str(request.url_rule), request.headers.get(prop.UUID), 
                str(datetime.timestamp(now)).replace(".", '')[:13:]
                )

    '''
        Builds an error response from the http 403 status code

        @error as the exception.
    '''
    @exception.app_errorhandler(Forbidden)
    def handle_forbidden(error):
        now = datetime.now()
        return GlobalExceptionHandler.__build_response(ErrorType.INVALID.name, 
                str(http.FORBIDDEN.value), 
                prop_exc.EXC_FORBIDDEN_DETAILS, 
                prop_exc.EXC_FORBIDDEN_LOCATION, 
                str(request.url_rule), request.headers.get(prop.UUID), 
                str(datetime.timestamp(now)).replace(".", '')[:13:]
                )

    '''
        Builds an error response from the http 404 status code

        @error as the exception.
    '''
    @exception.app_errorhandler(NotFound)
    def handle_not_found(error):
        now = datetime.now()
        return GlobalExceptionHandler.__build_response(ErrorType.INVALID.name, 
                str(http.NOT_FOUND.value), 
                prop_exc.EXC_NOT_FOUND_DETAILS, 
                prop_exc.EXC_NOT_FOUND_LOCATION, 
                str(request.url_rule), request.headers.get(prop.UUID), 
                str(datetime.timestamp(now)).replace(".", '')[:13:]
                )

    '''
        Builds an error response from the http 404 status code

        @error as the exception.
    '''
    @exception.app_errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        now = datetime.now()
        return GlobalExceptionHandler.__build_response(ErrorType.INVALID.name, 
                str(http.NOT_FOUND.value),
                prop_exc.EXC_METHOD_NOT_ALLOWED_DETAILS, 
                prop_exc.EXC_METHOD_NOT_ALLOWED_LOCATION, str(request.url_rule), 
                request.headers.get(prop.UUID), 
                str(datetime.timestamp(now)).replace(".", '')[:13:]
                )
             
    '''
        Builds an error response from the a Generic Exception

        @error as the exception.
    '''
    @exception.app_errorhandler(GenericException)
    def handle_generic_exception(exception):
        return GlobalExceptionHandler.__build_response(exception.error_type, exception.code, 
                exception.details, exception.location, exception.more_info, exception.uuid, 
                exception.timestamp)

    '''
        Builds an error response from the BadRequest Exception

        @type_ex as the type of error from {ERROR, WARN, INVALID, FATAL}
        @code as the httpstatus code
        @details as the details of the exception
        @location as the location where the exception occurred
        @more_info as the URI of the request
    '''
    def __build_response(type_ex, code, details, location, more_info, uuid, timestamp):
        error_response = ErrorResponse(
            type_ex, code, details, location, more_info, uuid, timestamp)
        response_data = json.dumps(error_response.__dict__)
        log.error(details)
        return Response(response = response_data, status = code, 
                        mimetype = prop.RESPONSE_FORMAT)