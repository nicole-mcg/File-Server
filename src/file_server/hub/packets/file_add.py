from file_server.hub.packet import Packet
from file_server.util.byte_buffer import ByteBuffer

from file_server.util import get_file_size

class FileAddPacket(Packet):
    name = "FileAddPacket"
    id = 2

    def __init__(self, hub=None, **kwargs):
        Packet.__init__(self, hub, **kwargs)

    def handle_outgoing(self, hub, file_sock):
        file_sock.send_file(self.file_name)

    def handle_incoming(self):
        self.file_sock.save_file()

    def handle_response(self, payload):
        pass

