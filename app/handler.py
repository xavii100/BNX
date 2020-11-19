from app.service_impl import ServiceImpl
from app.properties import Properties
from app.log import log
from app import utils

from watchdog.events import  FileSystemEventHandler
import time
import os

prop = Properties()
service = ServiceImpl()
SUCCESS = 1

class HandlerInbox(FileSystemEventHandler):
    
    @staticmethod
    def on_created(event):
        if os.path.exists(event.src_path):
            path_dir_names = prop.INBOX_PATH

            inbox_path = utils.get_path_from_list(*path_dir_names)
            file_name = event.src_path.replace(inbox_path,'')

            file_name = file_name.replace('\\','')
            file_name = file_name.replace('/','')

            log.info('File %s Arrived inbox',file_name)
            service.send_file(file_name)
            return SUCCESS
    
class HandlerOutbox(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        rejected_list = prop.REJECTED_FOLDERS
        oubox_path_dir_names = prop.OUTBOX_PATH.copy()
        path_dir_names = prop.OUTBOX_PATH

        outbox_path = utils.get_path_from_list(*path_dir_names)
        final_path = event.src_path.replace(outbox_path,'')

        folder_date, file_name = utils.get_outbox_file_name(final_path)

        oubox_path_dir_names.append(folder_date)

        log.info('File %s Arrived outbox',file_name)
        if not file_name.startswith('~') and not any([x in final_path for x in rejected_list]):
            log.info('Date Folder %s', folder_date)
            service.orchestrate_file(oubox_path_dir_names, file_name)
            return SUCCESS
        else:
            log.info('Cannot start orquestrate process with %s', file_name)
            return False
        
    