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

#from .file_observer import FileObserver
from watchdog.observers import Observer

from .event_handler import EventHandler

from datetime import datetime
#from .file_observer import AsynchronousObserver

from file_server.packet.impl import FileChangePacket, FileAddPacket

KILOBYTE = 1024

class FileProcessor(HubProcessor):
    def __init__(self, directory):
        self.directory = directory
        self.buffer_queue = {};
        self.packet_queue = None
        self.event_handler = None
        self.observer = None;
        self.block_start_time = datetime.now().microsecond
        self.block_end_time = self.block_start_time

    def initialize(self, packet_queue):
        self.packet_queue = packet_queue
        self.event_handler = EventHandler(self, self.directory)

        observer = Observer()
        observer.schedule(self.event_handler, self.directory, recursive=True)
        observer.start()

        self.observer = observer

    def shutdown(self):
        self.observer.join();

    #FIXME abstract this into HubProcessor
    def queue_packet(self, packet, data):
        if not data in self.buffer_queue:
            self.buffer_queue[data] = packet
        else:
            print("skipped duplicate packet")

    def get_file_size(self, file_name):
        return os.path.getsize(self.directory + file_name)

    def send_file(self, file_name, sock):

        file_size = self.get_file_size(file_name)

        sock.send(ByteBuffer.from_int(file_size).bytes())
        sock.send(ByteBuffer.from_string(file_name).bytes())

        with open(self.directory + file_name, mode='rb') as file:

            while(file_size > 0):
                chunk_size = KILOBYTE if file_size > KILOBYTE else file_size
                chunk = file.read(chunk_size)
                sock.send(chunk)
                file_size -= chunk_size


    def save_file(self, sock, length):

        file_size = ByteBuffer(sock.recv(4)).read_int()
        length -= 4

        name_length = length - file_size
        file_name = ByteBuffer(sock.recv(name_length)).read_string()
        length -= name_length

        file_path = self.directory + file_name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file = open(file_path,'wb')

        while(length > 0):
            self.event_handler.add_ignore(("change", file_name))
            chunk_size = KILOBYTE if length > KILOBYTE else length
            file.write(ByteBuffer(sock.recv(chunk_size)).bytes())
            length -= chunk_size

        file.close()

    def delete_file(self, file_name):
        print("Deleting File: " + file_name)
        file_path = self.directory + file_name
        try:
            if (os.path.isdir(file_path)):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        except OSError as e:
            pass

    def move_file(self, file_name, new_name):

        print("Moving File '{}' to '{}'".format(file_name, new_name))

        try:
            os.rename(self.directory + file_name, self.directory + new_name)
        except OSError as e:
            print(e)
            pass

    def pre(self, packet_queue):

        # Handle local events and send packets
        while len(self.buffer_queue.keys()) > 0:
            key = list(self.buffer_queue.keys())[0]
            self.packet_queue.queue_packet(self.buffer_queue[key])
            del self.buffer_queue[key]

        self.block_start_time = datetime.now().microsecond
        self.block_end_time = self.block_start_time

    def process(self, packet_queue):
        pass

    def post(self, packet_queue):
        self.block_end_time = datetime.now().microsecond
        