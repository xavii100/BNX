from app.service_impl import ServiceImpl
from app.properties import Properties
from app.log import log
from app import utils

import os
from watchdog.observers import Observer
import time

service = ServiceImpl()
prop = Properties()

class Listener():

    def __init__(self):
        self.observer_inbox = Observer()
        self.observer_outbox = Observer()

    def check_outbox(self):    
        try:
            path_dir_names = prop.INBOX_PATH
            path_inbox = utils.get_path_from_list(*path_dir_names)
            log.info('Starting listener inbox on %s', path_inbox)
            while True:
                self.start_listener(path_inbox)
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

    def start_listener(self, path_inbox):
        directories = os.listdir(path_inbox)
        if len(directories) != 0:
            log.info('Files were found in the directory %s', directories)
            self.send_files_to_service(directories, path_inbox)
    
    def send_files_to_service(self, directories, path_inbox):
        for file_name in directories:
            if self.is_valid_file(file_name, path_inbox):
                service.send_file(file_name)

    def is_valid_file(self, file_name, path):
        final_path = utils.append_file_name_to_path(path, file_name)
        if os.path.exists(final_path) and os.path.isfile(final_path):
            size = os.path.getsize(final_path)
            if size > 0:
                return True
        return False
