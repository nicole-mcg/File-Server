from file_server.hub.packet import Packet
from file_server.util.byte_buffer import ByteBuffer

from file_server.util import get_file_size

# Used to handle protocol for sending file changes
class FileChangePacket(Packet):
    name = "FileChangePacket"
    id = 1
    
    # hub: the FileHub associated with this packet
    # file_sock: the file_socket associated with the hub
    # length: the length of the packet
    # kwargs: exclusively for sending packets, sets properties in class for use later
    def __init__(self, hub=None, length=0, **kwargs):
        Packet.__init__(self, hub, length, **kwargs)

    def size(self):
        return get_file_size(self.hub.directory + self.file_name) + len(self.file_name) + 5;

    def handle_outgoing(self, hub, file_sock):
        file_sock.send_file(self.file_name)

    def handle_incoming(self):
        self.file_sock.save_file(self.length)

    def handle_response(self, payload):
        pass

