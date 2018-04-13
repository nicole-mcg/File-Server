import os, shutil

def get_file_size(file_name):
        return os.path.getsize(self.directory + file_name)

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