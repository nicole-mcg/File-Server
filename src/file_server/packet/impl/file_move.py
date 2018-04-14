from file_server.packet import Packet
from file_server.io import ByteBuffer

from file_server.util import move_file

class FileMovePacket(Packet):
    name = "FileMovePacket"
    id = 4
    def __init__(self, hub=None, easy_sock=None, length=0, **kwargs):
        super(self.__class__, self).__init__(hub, easy_sock, length)

        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
            self.new_name = kwargs["new_name"]

    def size(self):
        return len(self.file_name) + len(self.new_name) + 6;

    def handle_outgoing(self, hub, easy_sock):

        buff = ByteBuffer.from_string(self.file_name)
        buff.write_string(self.new_name)

        easy_sock.sock.send(buff.bytes())

    def handle_incoming(self):

        buff = ByteBuffer(self.easy_sock.sock.recv(self.length))

        file_name = buff.read_string()
        new_name = buff.read_string()

        self.hub.file_event_handler.add_ignore(("move", file_name, new_name))

        move_file(self.hub.directory + file_name, self.hub.directory + new_name)

    def handle_response(self, payload):
        pass

