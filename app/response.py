class ErrorResponse():

    def __init__(self, type_code, code, details, location, more_info, uuid, timestamp):
        self.type = type_code
        self.code = code
        self.details = details
        self.location = location
        self.more_info = more_info
        self.uuid = uuid
        self.timestamp = timestamp
