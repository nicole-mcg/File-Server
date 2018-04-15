from file_server.hub.packet import Packet
from file_server.util.byte_buffer import ByteBuffer

from file_server.util import get_file_size

# Used to handle protocol for sending and recieving file changes
class FileChangePacket(Packet):
    name = "FileChangePacket"
    id = 1
    
    # hub: the FileHub associated with this packet
    # kwargs: exclusively for outgoing packets {
    #     file_name: name of changed local file     
    # }
    def __init__(self, hub=None, **kwargs):
        Packet.__init__(self, hub, **kwargs)

    # Handles an outgoing packet
    def handle_outgoing(self, hub, file_sock):
        file_sock.send_file(self.file_name)

    # Handles an incoming packet
    def handle_incoming(self):
        self.file_sock.save_file()