from app.properties import Properties

import os

properties = Properties()

def return_outbox_path(date_path):
    outbox_path = properties.OUTBOX_PATH.copy()
    outbox_path.insert(len(outbox_path), date_path)
    return outbox_path

def append_file_name_to_path(path, file_name):
    final = ""
    if os.name == "nt":
        final = path + "\\" + file_name
    else:
        final = path + "/" + file_name
    return final


def get_path_from_list(*argv):
    final = ""
    base_path = os.environ.get('BASE_PATH')
    
    if base_path is None:
        base_path = "C:"
    if os.name == "nt":
        final = "{}\\{}".format(base_path, "\\".join(argv))
    else:
        final = "{}/{}".format(base_path, "/".join(argv))
    return final
