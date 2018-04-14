from file_server.file.packet.packet import Packet
from file_server.file.io import ByteBuffer

from file_server.util import get_file_size

class FileChangePacket(Packet):
    name = "FileChangePacket"
    id = 1
    def __init__(self, hub=None, easy_sock=None, length=0, **kwargs):
        super(self.__class__, self).__init__(hub, easy_sock, length)

        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]

    def size(self):
        return get_file_size(self.hub.directory + self.file_name) + len(self.file_name) + 5;

    def handle_outgoing(self, hub, easy_sock):
        easy_sock.send_file(self.file_name)

    def handle_incoming(self):
        self.easy_sock.save_file(self.length)

    def handle_response(self, payload):
        pass

