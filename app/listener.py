from app.service_impl import ServiceImpl
from app.properties import Properties
from app.log import log
from app import utils

import os
import time

service = ServiceImpl()
prop = Properties()

class Listener():

    def check_outbox(self):    
        try:
            path_dir_names = prop.INBOX_PATH
            path_inbox = utils.get_path_from_list(*path_dir_names)
            log.info('Starting listener inbox on %s', path_inbox)
            while True:
                self.start_listener(path_inbox)
                time.sleep(prop.TIME_WAITED)
        except KeyboardInterrupt:
            self.observer.stop()

    def start_listener(self, path_inbox):
        directories = os.listdir(path_inbox)
        if len(directories) != 0:
            log.info('Files were found in the directory %s', directories)
            self.send_files_to_service(directories, path_inbox)
    
    def send_files_to_service(self, directories, path_inbox):
        for file_name in directories:
            service.send_file(file_name)
