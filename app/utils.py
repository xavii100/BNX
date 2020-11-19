import os

'''
    Function to create a new folder.

    @folder_name as the new folder name.
    @path as the full path.
    @return True if the folder is created otherwise False.
'''
def create_folder(folder_name):
    mode = 0o666
    os.mkdir(folder_name, mode)

def get_path_from_list(*argv):
    final = ""
    os.environ["BASE_PATH"] = "C:"
    if os.name == "nt":
        # C:\carpeta\carpeta\carpeta
        final = "{}\\{}".format(os.environ.get('BASE_PATH'), "\\".join(argv))
    else:
        # /app/carpeta/carpeta
        final = "{}/{}".format(os.environ.get('BASE_PATH'), "/".join(argv))
    return final

def get_outbox_file_name(final_path):
    if os.name == "nt":
        # C:\carpeta\carpeta\carpeta
        path_dir_names = final_path.split('\\')
    else:
        path_dir_names = final_path.split('/')
        # /app/carpeta/carpeta
    print(path_dir_names)
    return path_dir_names[-2], path_dir_names[-1]
