
import os

from .network_util import send_post_request, send_api_request

#Attributes should be a dict: {"attr_name": "attr_value"}
def create_object(attributes):
    new_object = lambda: None #Used to create an object that we can apply attributes to
    for key in attributes.keys():
        setattr(new_object, key, attributes[key])
    return new_object

# https://stackoverflow.com/questions/13766513/how-to-do-force-remove-in-python-like-rm-rf-on-linux
def nuke_dir(dir):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            nuke_dir(path)
        else:
            os.unlink(path)
    os.rmdir(dir)

def split_path(file_path):
    allparts = []
    while 1:
        parts = os.path.split(file_path)
        if parts[0] == file_path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == file_path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            file_path = parts[0]
            if parts[1] != "":
                allparts.insert(0, parts[1])
    return allparts