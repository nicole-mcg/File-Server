import os, shutil

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

def get_file_size(file_name):
        return os.path.getsize(file_name)

def move_file(file_name, new_name):

        print("Moving File '{}' to '{}'".format(file_name, new_name))

        try:
            os.rename(file_name, new_name)
        except OSError as e:
            print(e)
            pass

def delete_file(file_name):
        print("Deleting File: " + file_name)

        try:
            if (os.path.isdir(file_name)):
                shutil.rmtree(file_name)
            else:
                os.remove(file_name)
        except OSError as e:
            pass