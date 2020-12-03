from app.client import ClientCommonFramework as client_common_framework
from app.properties import Properties
from app.service import Service
from app.log import log
from app import utils

properties = Properties()
SUCCESS = 1
FAILED = 0

class ServiceImpl(Service, object):

    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = object.__new__(self)
        return self._instance

    def send_file(self, file_name):
        log.info('Calling Common Framework move_api')
        path_dir_names = properties.INBOX_PATH
        response = client_common_framework.common_framework(path_dir_names, 
            file_name)
        log.info('Common Framework move_api was called')        
        if response is not None:
            log.info('Common Framework response: %s', response.status_code)
            if response.status_code == 200:
                log.info('Common Framework Call Successful')
                data = response.json()
                log.info('Common Framework response data: %s', data)
                
                path = data['date_folder']
                file_name = data['file_name']
        
                return self.orchestrate_file(path, file_name)
            elif response.status_code != 500:
                data = response.json()
                message = data['details']

                log.info('Common Framework response: %s',message)
                return FAILED
            else: 

                log.info('Common framework did not send a readable message')
                return FAILED
    
    def orchestrate_file(self, date_path, file_name):
        log.info('Appending outbox path with date_path')
        path = utils.return_outbox_path(date_path)
        log.info('Append return %s', path)

        log.info('Calling Orchestrate API')
        response = client_common_framework.orquestrate(path, 
            file_name)
        log.info('Orchestrate API was called successfully')

        if response is not None:
            log.info('Orchestrate API response: %s', response.status_code)
            if response.status_code == 200:

                log.info('Orchestrate process successful')
                return SUCCESS
            elif response.status_code != 500:
                data = response.json()
                message = data['details']

                log.info('Orchestrate process response: %s',message)
                return FAILED
            else: 
                log.info('Orchestrate API did not send a readable message')
                return FAILED

