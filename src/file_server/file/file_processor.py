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

from .file_observer import FileObserver

from .event_handler import EventHandler
#from .file_observer import AsynchronousObserver

class FileProcessor(HubProcessor):
    def __init__(self, directory):
        self.accepting_packets = True
        self.directory = directory
        self.buffer_queue = deque();
        self.packet_queue = None
        self.event_handler = None
        self.observer = None;

    def initialize(self, packet_queue):
        self.packet_queue = packet_queue
        self.event_handler = EventHandler(packet_queue, self.directory)

        observer = FileObserver()
        observer.schedule(self.event_handler, self.directory, recursive=True)
        observer.start()

        self.observer = observer

    def shutdown(self):
        self.observer.join();

    #FIXME abstract this into HubProcessor
    def queue_packet(self, packet):
        if (self.accepting_packets):
            self.packet_queue.queue_packet(packet)
        else:
            buffer_queue.append(packet)

    # FIXME move create_file, save_file, delete_file
    def create_file(self, file_name, file_contents):

        with self.observer._lock:
            self.observer.accepting_events = False

        print("Creating New File: " + file_name)
        self.save_file(file_name, file_contents)
        self.observer.accepting_events = True

        print("created file")

    def save_file(self, file_name, file_contents):

        with self.observer._lock:
            self.observer.accepting_events = False

        print("Updating Modified File: " + file_name)
        #with self.observer.ignore_events():
        file_path = self.directory + file_name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file = open(file_path,'wb')
        file.write(file_contents)
        file.close()
        self.observer.accepting_events = True

    def delete_file(self, file_name):

        with self.observer._lock:
            self.observer.accepting_events = False

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

            self.observer.accepting_events = True

    def move_file(self, file_name, new_name):

        print("Moving File '{}' to '{}'".format(file_name, new_name))

        with self.observer._lock:
            self.observer.accepting_events = False

        try:
            os.rename(self.directory + file_name, self.directory + new_name)
        except OSError as e:
            print(e)
            pass
        self.observer.accepting_events = True

    def pre(self, packet_queue):

        self.accepting_packets = False

        # Handle local events and send packets
        while len(self.buffer_queue) > 0:
            print("queued buffered packet")
            self.packet_queue.queue_packet(buffer_queue.pop())

        self.accepting_packets = True

    def process(self, packet_queue):
        pass

    def post(self, packet_queue):
        self.pre(packet_queue)
        