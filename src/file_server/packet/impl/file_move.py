from file_server.packet import Packet
from file_server.io import ByteBuffer

from file_server.util import move_file

class FileMovePacket(Packet):
    name = "FileMovePacket"
    id = 4
    def __init__(self, file_processor, easy_sock=None, length=0, hub=None, **kwargs):
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
            self.new_name = kwargs["new_name"]
        super(self.__class__, self).__init__(easy_sock, length)
        self.file_processor = file_processor
        self.easy_sock = easy_sock
        self.length = length
        self.hub = None

    def size(self):
        return len(self.file_name) + len(self.new_name) + 6;

    def handle_outgoing(self, easy_sock, hub):

        buff = ByteBuffer.from_string(self.file_name)
        buff.write_string(self.new_name)

        easy_sock.sock.send(buff.bytes())

    def handle_incoming(self):
        buff = ByteBuffer(self.easy_sock.sock.recv(self.length)) if self.length > 0 else None



        file_name = buff.read_string()
        new_name = buff.read_string()

        self.file_processor.event_handler.add_ignore(("move", file_name, new_name))

        move_file(self.file_processor.directory + file_name, self.file_processor.directory + new_name)

    def handle_response(self, payload):
        pass

