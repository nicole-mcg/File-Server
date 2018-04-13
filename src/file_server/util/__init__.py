
import os


from .network_util import send_post_request
from .file_util import get_file_size, move_file, delete_file

# Attributes should be a dict: {"attr_name": "attr_value"}
def create_object(attributes):
    new_object = lambda: None #Used to create an object that we can apply attributes to
    for key in attributes.keys():
        setattr(new_object, key, attributes[key])
    return new_object

# Splits a file path into parts
# Should work with any path on any os
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