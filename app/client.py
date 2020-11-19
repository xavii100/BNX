from app.properties import Properties
from app.log import log
import requests as req

prop = Properties()

class ClientCommonFramework(object):

    def common_framework(path_dir_names, file_name):
        data = {
            'file_name': file_name, 
            'path_dir_names': path_dir_names
        }                    
        
        headers = {
            "accept": "application/json", 
            "content-type": "application/json", 
            "uuid": prop.UUID
        }
        response = ClientCommonFramework.post_request(prop.COMMON_FRAMEWORK_API, data, 
            headers)
        return response

    def orquestrate(path_dir_names, file_name):
        data = {
            'file_name': file_name, 
            'path_dir_names': path_dir_names
        }                    
        
        headers = {
            "accept": "application/json", 
            "content-type": "application/json", 
            "uuid": prop.UUID,
            "content-language": prop.CONTENT_LANGUAGE
        }
        response = ClientCommonFramework.post_request(prop.ORCHESTRATE_API, data, 
            headers)
        return response

    def post_request(resource, request_data, headers):
        try:
            URI = prop.COMMON_FRAMEWORK_URI + prop.COMMON_FRAMEWORK_PREFIX + resource
            return req.post(URI, json = request_data, headers = headers)
        except ConnectionError:
            log.info('Connection Error with Common Framework')
            return None
