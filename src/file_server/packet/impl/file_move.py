from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileMovePacket(Packet):
    name = "FileMovePacket"
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
        return len(self.file_name) + len(self.new_name) + 6;

    def handle_outgoing(self, sock):

        print("old name=" + self.file_name)
        print("new name=" + self.new_name)

        buff = ByteBuffer.from_string(self.file_name)
        buff.write_string(self.new_name)

        sock.send(buff.bytes())

    def handle_incoming(self):
        buff = ByteBuffer(self.sock.recv(self.length)) if self.length > 0 else None



        file_name = buff.read_string()
        new_name = buff.read_string()

        self.hub_processor.event_handler.add_ignore(("move", file_name, new_name))

        print("old name=" + file_name)
        print("new name=" + new_name)

        self.hub_processor.move_file(file_name, new_name)

    def handle_response(self, payload):
        pass

