from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileMovePacket(Packet):
    name = "FileDeletePacket"
    id = 4
    def __init__(self, hub_processor, sock=None, length=0, **kwargs):
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
            self.new_name = kwargs["new_name"]
        super(self.__class__, self).__init__(sock, length)
        self.hub_processor = hub_processor
        self.sock = sock
        self.length = length

    def size(self):
        return len(self.file_name) + 5;

    def handle_outgoing(self):
        buff = ByteBuffer.from_string(self.file_name)
        buff.write_string(self.new_name)

        self.sock.send(ByteBufer.from_int(len(b)).bytes())
        self.sock.send(buff.bytes())

    def handle_incoming(self,):
        buff = ByteBuffer(self.sock.recv(self.length)) if length > 0 else None

        file_name = buff.read_string()
        new_name = buff.read_string()

        self.hub_processor.move_file(file_name, new_name)

    def handle_response(self, payload):
        pass

