import os, shutil
from collections import deque

from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
from watchdog.events import (
    DirMovedEvent,
    DirDeletedEvent,
    DirCreatedEvent,
    DirModifiedEvent,
    FileMovedEvent,
    FileDeletedEvent,
    FileCreatedEvent,
    FileModifiedEvent
)

from file_server import HubProcessor
from file_server.io import ByteBuffer

from .event_handler import EventHandler
#from .file_observer import AsynchronousObserver

class FileProcessor(HubProcessor):
    def __init__(self, directory):
        self.directory = directory
        self.event_handler = None
        self._take_snapshot = lambda: DirectorySnapshot(self.directory, True)
        self._snapshot = self._take_snapshot()
        self.event_handler = None

    def create_file(self, file_name, file_contents):
        print("Creating New File: " + file_name)
        self.save_file(file_name, file_contents)

    def save_file(self, file_name, file_contents):
        print("Updating Modified File: " + file_name)
        #with self.observer.ignore_events():
        file_path = self.directory + file_name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file = open(file_path,'wb')
        file.write(file_contents)
        file.close()

    def delete_file(self, file_name):
        print("Deleting File: " + file_name)
        file_path = self.directory + file_name
        #with self.observer.ignore_events():
        try:
            if (os.path.isdir(file_path)):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        except OSError as e:
            pass

    def move_file(self, file_name, new_name):
        print("Moving File '{}' to '{}'".format(file_name, new_name))
        #with self.observer.ignore_events():
        try:
            os.rename(self.directory + file_name, self.directory + new_name)
        except OSError as e:
            print(e)
            pass

    def pre(self, packet_queue):
        if (self.event_handler is None):
            self.event_handler = EventHandler(packet_queue, self.directory)

        event_queue = deque()

        # Get event diff between fresh snapshot and previous snapshot.
        # Update snapshot.
        try:
            new_snapshot = self._take_snapshot()
        except OSError as e:
            event_queue.append(DirDeletedEvent(self.watch.path))
            self.stop()
            return
        except Exception as e:
            raise e

        events = DirectorySnapshotDiff(self._snapshot, new_snapshot)
        self._snapshot = new_snapshot

        # Files.
        for src_path in events.files_deleted:
            event_queue.append(FileDeletedEvent(src_path))
        for src_path in events.files_modified:
            event_queue.append(FileModifiedEvent(src_path))
        for src_path in events.files_created:
            event_queue.append(FileCreatedEvent(src_path))
        for src_path, dest_path in events.files_moved:
            event_queue.append(FileMovedEvent(src_path, dest_path))

        # Directories.
        for src_path in events.dirs_deleted:
            event_queue.append(DirDeletedEvent(src_path))
        for src_path in events.dirs_modified:
            event_queue.append(DirModifiedEvent(src_path))
        for src_path in events.dirs_created:
            event_queue.append(DirCreatedEvent(src_path))
        for src_path, dest_path in events.dirs_moved:
            event_queue.append(DirMovedEvent(src_path, dest_path))

        while len(event_queue) > 0:
            self.event_handler.dispatch(event_queue.pop())

    def process(self, packet_queue):
        self._snapshot = self._take_snapshot() # FIXME This should handle the directory being deleted

    def post(self, packet_queue):
        self.pre(packet_queue)
        