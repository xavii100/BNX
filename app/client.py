from app.properties import Properties
from app.log import log
import requests as req

prop = Properties()

class ClientCommonFramework(object):

    def common_framework(path_dir_names, file_name):
        log.info('Creating request to common framework client move_api with path: %s and \
                file_name: %s', path_dir_names, file_name)
        data = {
            'file_name': file_name, 
            'path_dir_names': path_dir_names
        }                    
        
        log.info('Creating headers of request common framework move_api')
        headers = {
            "accept": "application/json", 
            "content-type": "application/json", 
            "uuid": prop.UUID
        }
        log.info('headers common framework client move_api created %s', headers)

        response = ClientCommonFramework.post_request(prop.COMMON_FRAMEWORK_API, data, 
            headers)
        return response

    def orquestrate(path_dir_names, file_name):
        log.info('Creating request to common framework client move_api with path: %s and \
                file_name: %s', path_dir_names, file_name)
        data = {
            'file_name': file_name, 
            'path_dir_names': path_dir_names
        }                    
        
        log.info('Creating headers of request common framework client orchestrate_api')
        headers = {
            "accept": "application/json", 
            "content-type": "application/json", 
            "uuid": prop.UUID,
            "content-language": prop.CONTENT_LANGUAGE
        }
        log.info('headers common framework client created orchestrate_api %s', headers)

        response = ClientCommonFramework.post_request(prop.ORCHESTRATE_API, data, 
            headers)
        return response

    def post_request(resource, request_data, headers):
        try:
            URI = prop.COMMON_FRAMEWORK_URI + prop.COMMON_FRAMEWORK_PREFIX + resource
            return req.post(URI, json = request_data, headers = headers)
        except:
            log.info('Connection Error with Common Framework')
            return None
