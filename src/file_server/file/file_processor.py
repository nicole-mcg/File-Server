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


from file_server.io import ByteBuffer

from watchdog.observers import Observer

from .event_handler import EventHandler
from .snapshot import DirectorySnapshot

from time import time

from file_server.packet.impl import FileChangePacket, FileAddPacket

from file_server.util import get_file_size

class FileProcessor():
    def __init__(self, directory):
        self.directory = directory
        self.buffer_queue = {};
        self.packet_queue = None
        self.event_handler = None
        self.observer = None
        self.update_status = False
        self.snapshot = None

    def create_snapshot(self):
        self.snapshot = DirectorySnapshot(self.directory, "/", self.directory)

    def initialize(self, packet_queue):
        self.packet_queue = packet_queue
        self.event_handler = EventHandler(self, self.directory)

        self.create_snapshot()

        observer = Observer()
        observer.schedule(self.event_handler, self.directory, recursive=True)
        observer.start()

        self.observer = observer

    def shutdown(self):
        self.observer.join();

    def queue_packet(self, packet, data):
        packet.time = time()
        self.buffer_queue[data] = packet

    def pre(self, packet_queue):

        # Handle local events and send packets
        while len(self.buffer_queue.keys()) > 0:
            key = list(self.buffer_queue.keys())[0]
            packet = self.buffer_queue[key]

            # Check time to make sure any duplicate packets are picked up
            if time() - packet.time > 1:
                self.packet_queue.queue_packet(packet)
                del self.buffer_queue[key]

    def process(self, packet_queue):
        pass

    def post(self, packet_queue):
        pass