from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileDeletePacket(Packet):
    name = "FileDeletePacket"
    id = 3
    def __init__(self, file_processor, sock=None, length=0, conn=None, **kwargs):
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
        super(self.__class__, self).__init__(sock, length)
        self.file_processor = file_processor
        self.sock = sock
        self.length = length
        self.conn = conn

    def size(self):
        return len(self.file_name) + 5;

    def handle_outgoing(self, sock, conn):
        sock.send(ByteBuffer.from_string(self.file_name).bytes())

    def handle_incoming(self):

        buff = ByteBuffer(self.sock.recv(self.length)) if self.length > 0 else None
        file_name = buff.read_string()

        self.file_processor.event_handler.add_ignore(("delete", file_name))

        self.file_processor.delete_file(file_name)

    def handle_response(self, payload):
        pass

