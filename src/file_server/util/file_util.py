import os, shutil

# FIXME this function was stolen from StackOverflow and could probably be rewritten better
# Splits a file path into parts
# Should work with any path on any os
# file_path: the path to split
# returns a list of the parts gathered
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

# Gets the size of the specified file
# file_name: the path to the file
def get_file_size(file_name):
    return os.path.getsize(file_name)

# Renames a file and/or moves it to a new directory
# file_name: the path and name of the file to move
# new_name: the new path and name for the file 
def move_file(file_name, new_name):

    print("Moving File '{}' to '{}'".format(file_name, new_name))

    # Try to rename the file
    try:
        os.rename(file_name, new_name)
    except OSError as e:
        print("Error moving file")
        print(e)

# Deletes a file or folder (recursively)
# file_name: the path for the file or directory to delete
def delete_file(file_name):
    print("Deleting File: " + file_name)

    # Try to delete the file or folder
    try:
        if (os.path.isdir(file_name)):
            shutil.rmtree(file_name)
        else:
            os.remove(file_name)
    except OSError as e:
        print("Error deleting file")
        print(e)