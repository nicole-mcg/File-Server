from time import time

from watchdog.observers import Observer

from file_server.file import FileEventHandler, DirectorySnapshot
from file_server.io.easy_socket import EasySocket

class Hub:
    def __init__(self, directory, port=EasySocket.PORT):
        self.directory = directory
        self.port = port

        self.buffer_queue = {}

        self.file_event_handler = None
        self.file_observer = None

        self.directory_snapshot = None

    def initialize(self):

        self.directory_snapshot = DirectorySnapshot(self.directory, "/", self.directory)

        self.file_event_handler = FileEventHandler(self, self.directory)

        self.file_observer = Observer()
        self.file_observer.schedule(self.file_event_handler, self.directory, recursive=True)
        self.file_observer.start()

    def kill(self):
        
        # Shut down file watch
        if self.file_observer is not None:
            self.file_observer.stop()

    # Used to send a packet
    def send_packet(self, packet):
        pass

    # Adds a 
    def queue_packet(self, packet, data):
        packet.time = time()
        self.buffer_queue[data] = packet

    def prepare_packets(self, packet_queue):

        num_unready_packets = 0

        buffer_queue = list(self.buffer_queue.keys())

        for key in buffer_queue:
            packet = self.buffer_queue[key]

            # Wait at least 1 second before sending a packet
            # This is so that duplicates can be checked before sending (maybe this time should be longer)
            if time() - packet.time > 1:
                self.send_packet(packet)
                del self.buffer_queue[key]
            