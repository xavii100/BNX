from app.listener import Listener
import os

def test_listener(mocker):
    mocker.patch('app.listener.os.listdir', return_value = ['test_file'])
    mocker.patch('app.listener.service')
    listener = Listener()
    path = ['test', 'file_name_test']
    path = get_path_from_list(*path)
    listener.start_listener(path)


def get_path_from_list(*argv):
    final = ""
    
    if os.name == "nt":
        final =  "\\".join(argv)
    else:
        final = "/".join(argv)
    return final
