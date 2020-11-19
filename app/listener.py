from app.handler import HandlerInbox, HandlerOutbox
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
            event_handler = HandlerInbox()
            path_dir_names = prop.INBOX_PATH
            path_inbox = utils.get_path_from_list(*path_dir_names)
            log.info(path_inbox)
            log.info('Starting listener inbox')
            while True:
                self.start_listener(path_inbox)
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

    def start_listener(self, path_inbox):
        directories = os.listdir(path_inbox)
        if len(directories) != 0:
            print(directories)
            for file_name in directories:
                print(file_name)
                service.send_file(file_name)




    def check_file_inbox(self):
        event_handler = HandlerInbox()
        path_dir_names = prop.INBOX_PATH
        path = utils.get_path_from_list(*path_dir_names)
        log.info('Starting listener inbox')
        log.info(path)

        path_test = path_dir_names.copy()
        path_test.insert(len(path_test), 'Cat_Holding_20200506.txt')
        file1 = utils.get_path_from_list(*path_test)
        if os.path.exists(file1):
            log.info('%s exists', file1)
        else:
            log.info('%s does not exists', file1)


        path_test2 = path_dir_names.copy()
        path_test2.insert(len(path_test2), 'CargaPerRel_AyB_ENE20_.xlsx ')
        file2 = utils.get_path_from_list(*path_test2)
        if os.path.exists(file2):
            log.info('%s exists', file2)
        else:
            log.info('%s does not exists', file2)

        self.observer_inbox.schedule(event_handler, path, recursive = True)
        self.observer_inbox.start()

        event_handler_outbox = HandlerOutbox()
        path_dir_names_outbox = prop.OUTBOX_PATH
        path_outbox = utils.get_path_from_list(*path_dir_names_outbox)
        log.info('Starting listener outbox')
        log.info(path_outbox)

        self.observer_outbox.schedule(event_handler_outbox, path_outbox, recursive = True)
        self.observer_outbox.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join
    
