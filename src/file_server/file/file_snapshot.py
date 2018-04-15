import os
from enum import Enum

from file_server.util import split_path

# This class hold metadata for a file
# Parent class for DirectorySnapshot
class FileSnapshot:
    TYPE_DIRECTORY = 1
    TYPE_FILE = 2

    # Recursively captures metadata for files and folders in the directory
    # full_path: the path of the file to capture (including root_path)
    # file_name: the name of the file
    # root_path: the path of the root directory being watched. Used to give paths relative to file watch
    def __init__(self, full_path, file_name, root_path):
        self.full_path = full_path
        self.file_name = file_name
        self.rel_path = os.path.relpath(full_path, root_path).replace("\\", "/")
        self.last_modified = os.path.getmtime(full_path)

    # Returns the type of snapshot (File)
    def get_type(self):
        return FileSnapshot.TYPE_FILE

    # Used to update the metadata for the file
    def update(self):
        pass

    # Converts the metadata into a JSON format that can be sent via web
    def to_json(self):
        return '{"type": ' + str(self.get_type()) + ', "file_name": "' +  self.file_name + '", "full_path": "' + self.rel_path + '", "last_modified": ' + str(self.last_modified) + '}'

    # Convert to a string
    def __str__(self):
        return self.to_json()

# This class holds metadata for a directory tree
class DirectorySnapshot(FileSnapshot):

    # Recursively captures metadata for files and folders in the directory
    # full_path: the path of the directory to capture (including root_path)
    # file_name: the name of the directory
    # root_path: the path of the root directory being watched. Used to give paths relative to file watch
    def __init__(self, full_path, file_name, root_path):

        # Initialize parent class
        FileSnapshot.__init__(self, full_path, file_name, root_path)

        # The dict of child snapshots for files and folders in the directory
        # key: file name
        # value: FileSnapshot or DirectorySnapshot instance
        self.snapshots = {};

        # Loop through files in the directory
        for file in os.listdir(full_path):
            file_path = full_path + "/" + file

            # Default to FileSnapshot to represent the file
            cls = FileSnapshot

            # Use DirectorySnapshot to represent file if it's a directory
            if os.path.isdir(file_path):
                cls = DirectorySnapshot

            # Create the snapshot and add it to snapshots dict
            self.snapshots[file] = cls(file_path, file, root_path)

    # Gets the type of snapshot (Directory)
    def get_type(self):
        return FileSnapshot.TYPE_DIRECTORY
        
    # FIXME this method is not fully written
    # Used to update a file or folder within the directory
    # file_path: the path of the file to update (from the root directory)
    def update(self, file_path=""):

        parts = split_path(file_path)

        if parts[0] in self.snapshots.keys():
            self.snapshots[allparts[0]].update(file_path)

    # Converts a snapshot within the snapshot's directory tree to JSON
    # path: the path of the file or directory to convert
    # recursive: if true, directories on the path will be converted recursively
    def to_json(self, path="./", recursive=True):
        snapshots = self.snapshots

        # Split path into parts
        path_parts = split_path(path)

        # Loop through parts till we find a useful one
        for index, part in enumerate(path_parts):

            # Skip useless parts
            if part == "." or part == "":
                continue

            # Pass the job to a child snapshot
            return snapshots[part].to_json("/".join(path_parts[index:]))

        string = '{"type": ' + str(self.get_type()) + ', "file_name": "' +  self.file_name + '", "full_path": "' + self.rel_path + '", "last_modified": ' + str(self.last_modified) + ', "snapshots": ['

        # Recursively convert child snapshots to JSON
        for index, key in enumerate(snapshots.keys()):
            snapshot = snapshots[key]

            if not recursive and isinstance(snapshot, DirectorySnapshot):

                # Convert the DirectorySnapshot to JSON using FileSnapshot if not recursive
                string += FileSnapshot.__str__(snapshot)

            else:

                # Convert the snapshot to JSON using default method
                string += str(snapshot)

            # Add a comma if this isn't the last snapshot
            if index != len(snapshots) - 1:
                string +=  ","

        string += "]}"

        return string

    # Convert to a string
    def __str__(self):
        return self.to_json()