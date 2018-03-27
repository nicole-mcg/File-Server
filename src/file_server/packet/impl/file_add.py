from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileAddPacket(Packet):
    name = "FileAddPacket"
    id = 2
    def __init__(self, hub_processor, sock=None, length=0, **kwargs):
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
        super(self.__class__, self).__init__(sock, length)
        self.hub_processor = hub_processor
        self.sock = sock
        self.length = length

    def size(self):
        return self.hub_processor.get_file_size(self.file_name) + len(self.file_name) + 5;

    def handle_outgoing(self):
        self.hub_processor.send_file(self.file_name)

    def handle_incoming(self):
        self.hub_processor.save_file(self.sock, self.length)

    def handle_response(self, payload):
        pass

