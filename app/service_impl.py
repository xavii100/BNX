from app.client import ClientCommonFramework as client_common_framework
from app.properties import Properties
from app.service import Service
from app.log import log
from app import utils

properties = Properties()

class ServiceImpl(Service, object):

    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = object.__new__(self)
        return self._instance

    def send_file(self, file_name):
        log.info('Calling Common Framework')
        path_dir_names = properties.INBOX_PATH
        response = client_common_framework.common_framework(path_dir_names, 
            file_name)
        
        if response is not None:
            log.info('Common Framework response: %s', response.status_code)
            if response.status_code == 200:
                log.info('Common Framework Call Successful')
            elif response.status_code != 500:
                data = response.json()
                message = data['details']
                log.info('Common Framework response: %s',message)
            else: 
                log.info('Common framework did not send a readable message')
    
    def orchestrate_file(self, path, file_name):
        log.info('Calling Orchestrate API')
        response = client_common_framework.orquestrate(path, 
            file_name)

        if response is not None:
            log.info('Orchestrate API response: %s', response.status_code)
            if response.status_code == 200:
                log.info('Orchestrate process successful')
            elif response.status_code != 500:
                data = response.json()
                message = data['details']
                log.info('Orchestrate process response: %s',message)
            else: 
                log.info('Orchestrate API did not send a readable message')

