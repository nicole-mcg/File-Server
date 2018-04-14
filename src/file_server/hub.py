from time import time

from watchdog.observers import Observer

from file_server.file.event_handler import FileEventHandler
from file_server.file.file_snapshot import DirectorySnapshot
from file_server.file.file_socket import FileSocket

# This class contains code common for the FileServer and FileClient class
class FileHub:

    # directory: the directory to watch
    # port: the port for the connection
    def __init__(self, directory, port=FileSocket.PORT):
        self.directory = directory
        self.port = port

        # This is a buffer queue for packets before they are queued to be sent
        # It's used to check for duplicate packets
        self.buffer_queue = {}

        # FileEventHandler
        # The file watch event handler
        self.file_event_handler = None

        # Observer
        # The which watches the files
        self.file_observer = None

        # DirectorySnapshot
        # Metadata for the directory being watched
        self.directory_snapshot = None

    # Used to initialize the file watch
    def initialize(self):

        # Create a snapshot of the directory
        self.directory_snapshot = DirectorySnapshot(self.directory, "/", self.directory)

        # Create the event handler and observer
        self.file_event_handler = FileEventHandler(self, self.directory)
        self.file_observer = Observer()
        
        # Set info for the observer
        self.file_observer.schedule(self.file_event_handler, self.directory, recursive=True)

        # Starts observer on a new thread
        self.file_observer.start()

    # Used to completely shutdown the hub
    def kill(self):
        
        # Shut down file watch
        if self.file_observer is not None:
            self.file_observer.stop()

    # Used to send a packet to other connected hubs
    def send_packet(self, packet):
        pass

    # Queues a packet to be sent
    # The packet may not be sent if it is considered a duplicate
    def queue_packet(self, packet, data):
        packet.time = time()
        self.buffer_queue[data] = packet

    # Sends ready packets from the buffer_queue
    def prepare_packets(self, packet_queue):

        # Get a list of the keys in the buffer_queue
        # By creating a list object we can use a for loop while removing items from the real buffer_queue 
        buffer_queue = list(self.buffer_queue.keys())

        # Loop through keys in self.buffer_queue
        for key in buffer_queue:
            packet = self.buffer_queue[key]

            # Wait at least 1 second before sending a packet
            # This is so that duplicates can be checked before sending (maybe this time should be longer)
            if time() - packet.time > 1:

                # Send the packet on the connection
                self.send_packet(packet)

                # Remove the packet from the buffer queue
                del self.buffer_queue[key]
            