from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileChangePacket(Packet):
    name = "FileChangePacket"
    id = 1
    def __init__(self, file_processor, sock=None, length=0, conn=None, **kwargs):
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
        super(self.__class__, self).__init__(sock, length)
        self.file_processor = file_processor
        self.sock = sock
        self.length = length
        self.conn = conn

    def size(self):
        return self.file_processor.get_file_size(self.file_name) + len(self.file_name) + 5;

    def handle_outgoing(self, sock, conn):
        self.file_processor.send_file(self.file_name, sock, conn)

    def handle_incoming(self):
        self.file_processor.save_file(self.sock, self.length, self.conn)

    def handle_response(self, payload):
        pass

