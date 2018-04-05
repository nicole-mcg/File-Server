import os
from enum import Enum

class Snapshot:
    types = Enum("SnapshotType", "DIRECTORY FILE")

    def __init__(self, full_path, file_name, root_path):
        self.full_path = full_path
        self.file_name = file_name
        self.rel_path = os.path.relpath(full_path, root_path).replace("\\", "/")
        self.last_modified = os.path.getmtime(full_path)

    def update(self, file_path=""):
        pass

    def get_type(self):
        return Snapshot.types.FILE

    def __str__(self):
        return '{"type": ' + str(self.get_type().value) + ', "file_name": "' +  self.file_name + '", "full_path": "' + self.rel_path + '", "last_modified": ' + str(self.last_modified) + '}'

class FileSnapshot(Snapshot):

    def __init__(self, full_path, file_name, root_path):
        Snapshot.__init__(self, full_path, file_name, root_path)

    def update(self, file_path=""):
        Snapshot.update(self)

    def __str__(self):
        return Snapshot.__str__(self)

class DirectorySnapshot(Snapshot):

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
                allparts.insert(0, parts[1])
        return allparts


    def __init__(self, full_path, file_name, root_path):
        Snapshot.__init__(self, full_path, file_name, root_path)
        self.snapshots = {};
        self.add_path(full_path, root_path)
        print(str(self))

    def add_path(self, path, root_path):
        for file in os.listdir(path):
            file_path = self.full_path + "/" + file

            cls = FileSnapshot

            if os.path.isdir(file_path):
                print("Added dir" + file_path)
                cls = DirectorySnapshot
            else:
                print("Added file" + file_path)

            self.snapshots[file] = cls(file_path, file, root_path)

    def update(self, file_path=""):
        Snapshot.update(self)

        parts = DirectorySnapshot.split_path(file_path)

        if parts[0] in self.snapshots.keys():
            self.snapshots[allparts[0]].update(file_path)

    def get_type(self):
        return Snapshot.types.DIRECTORY

    def to_json(self, path="./", recursive=True):
        string = '{"type": ' + str(self.get_type().value) + ', "file_name": "' +  self.file_name + '", "full_path": "' + self.rel_path + '", "last_modified": ' + str(self.last_modified) + ', "snapshots": ['

        snapshots = self.snapshots

        print(path)
        path_parts = DirectorySnapshot.split_path(path)
        for index, part in enumerate(path_parts):
            if part == "." or part == "":
                continue
            if part in snapshots:
                return snapshots[part].to_json("/".join(path_parts[index:]))

        for index, key in enumerate(snapshots.keys()):
            snapshot = snapshots[key]
            if not recursive and isinstance(snapshot, DirectorySnapshot):
                string += Snapshot.__str__(snapshot)
            else:
                string += str(snapshot)
            if index != len(snapshots) - 1:
                string +=  ","
        string += "]}"
        return string

    def __str__(self):
        return self.to_json()