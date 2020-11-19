from app.handler import HandlerInbox, HandlerOutbox
from app.properties import Properties

import os

SUCCESS = 1

class TestHandlerInbox():

    handler = HandlerInbox()

    def test_on_created(self, mocker):
        self.mock_properties(mocker)
        mocker.patch('os.path.exists', return_value = True)
        mocker.patch('app.handler.ServiceImpl.send_file')
        event = EventMock('/inbox/Cat_Holding_20200530')

        response = self.handler.on_created(event)
        assert response == SUCCESS

    def mock_properties(self, mocker):
        path_inbox = ['TRR', 'inbox']
        mocker.patch.object(Properties, 'INBOX_PATH', path_inbox)

class TestHandlerOutbox():

    handler = HandlerOutbox()

    def test_on_created(self, mocker):
        self.mock_properties(mocker)
        mocker.patch('os.path.exists', return_value = True)
        mocker.patch('app.handler.ServiceImpl.orchestrate_file')
        event = mock_event()

        response = self.handler.on_created(event)
        assert response == SUCCESS

    def test_rejected_folder(self, mocker):
        self.mock_properties(mocker)
        mocker.patch('os.path.exists', return_value = True)
        mocker.patch('app.handler.ServiceImpl.orchestrate_file')
        event = mock_event_rejected_folder()

        response = self.handler.on_created(event)
        assert response == False

    def test_trash_files_folder(self, mocker):
        self.mock_properties(mocker)
        mocker.patch('os.path.exists', return_value = True)
        mocker.patch('app.handler.ServiceImpl.orchestrate_file')
        event = mock_trash_files_folder()

        response = self.handler.on_created(event)
        assert response == False

    def mock_properties(self, mocker):
        path_outbox = ['TRR', 'outbox']
        rejected_folders = ['REJ', 'TRASH_FILES']

        mocker.patch.object(Properties, 'OUTBOX_PATH', path_outbox)
        mocker.patch.object(Properties, 'REJECTED_FOLDERS', rejected_folders)

def mock_trash_files_folder():
    if os.name == "nt":
        return EventMock('\\outbox\\TRASH_FILES\\Cat_Holding_20200530')
    else:
        return EventMock('/outbox/TRASH_FILES/Cat_Holding_20200530')

def mock_event_rejected_folder():
    if os.name == "nt":
        return EventMock('\\outbox\\REJ\\20200530\\Cat_Holding_20200530')
    else:
        return EventMock('/outbox/REJ/20200530/Cat_Holding_20200530')

def mock_event():
    if os.name == "nt":
        return EventMock('\\outbox\\20200530\\Cat_Holding_20200530')
    else:
        return EventMock('/outbox/20200530/Cat_Holding_20200530')

class EventMock():

    def __init__(self, src_path):
        self.src_path = src_path
