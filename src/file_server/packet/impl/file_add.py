from file_server.packet import Packet
from file_server.io import ByteBuffer

from file_server.util import get_file_size

class FileAddPacket(Packet):
    name = "FileAddPacket"
    id = 2
    def __init__(self, file_processor, easy_sock=None, length=0, hub=None,**kwargs):
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
        super(self.__class__, self).__init__(easy_sock, length)
        self.file_processor = file_processor
        self.easy_sock = easy_sock
        self.length = length
        self.hub = hub

    def size(self):
        return get_file_size(self.file_processor.directory + self.file_name) + len(self.file_name) + 5;

    def handle_outgoing(self, easy_sock, hub):
        easy_sock.send_file(self.file_name)

    def handle_incoming(self):
        self.easy_sock.save_file(self.length)

    def handle_response(self, payload):
        pass

