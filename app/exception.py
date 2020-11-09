from app.properties import Properties
from app.custom_enum import ErrorType 

from http import HTTPStatus as http
from datetime import datetime
from flask import request

properties = Properties()

class GenericException(Exception):

    def __init__(self, error_type, code, details, location, more_info, uuid, timestamp):
        self.error_type = error_type
        self.code = code
        self.details = details
        self.location = location
        self.more_info = more_info
        self.uuid = uuid
        self.timestamp = timestamp

class BadRequest(GenericException):

    def __init__(self, details, location):
        error_type = ErrorType.INVALID.name
        code = str(http.BAD_REQUEST.value)
        more_info = str(request.url_rule)
        uuid = request.headers.get(properties.UUID)
        now = datetime.today()
        timestamp = str(datetime.timestamp(now)).replace(".", '')[:13:]
        GenericException.__init__(self, error_type, code, details, location, 
            more_info, uuid, timestamp)
