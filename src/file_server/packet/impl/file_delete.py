from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileDeletePacket(Packet):
    name = "FileDeletePacket"
    id = 3
    def __init__(self, hub_processor, sock=None, length=0, **kwargs):
        if "file_name" in kwargs:
            self.file_name = ByteBuffer.from_string(kwargs["file_name"]).bytes()
        super(self.__class__, self).__init__(sock, length)
        self.hub_processor = hub_processor
        self.sock = sock
        self.length = length

    def size(self):
        return len(self.file_name) + 5;

    def handle_outgoing(self):
        b = ByteBuffer.from_string(self.file_name).bytes()
        self.sock.send(ByteBuffer.from_int(len(b)).bytes())
        self.sock.send(b)

    def handle_incoming(self):

        buff = ByteBuffer(self.sock.recv(self.length)) if length > 0 else None
        file_name = buff.read_string()

        self.hub_processor.delete_file(file_name)

    def handle_response(self, payload):
        pass

