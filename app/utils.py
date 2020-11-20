import os

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
