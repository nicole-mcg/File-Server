from file_server.hub.packet import Packet
from file_server.util.byte_buffer import ByteBuffer
from file_server.util import move_file

class FileMovePacket(Packet):
    name = "FileMovePacket"
    id = 4
    def __init__(self, hub=None, **kwargs):
        Packet.__init__(self, hub, **kwargs)

    def handle_outgoing(self, hub, file_sock):

        buff = ByteBuffer.from_string(self.file_name)
        buff.write_string(self.new_name)

        file_sock.sock.send(buff.bytes())

    def handle_incoming(self):

        buff = ByteBuffer(self.file_sock.sock.recv(self.length))

        file_name = buff.read_string()
        new_name = buff.read_string()

        self.hub.file_event_handler.add_ignore(("move", file_name, new_name))

        move_file(self.hub.directory + file_name, self.hub.directory + new_name)

    def handle_response(self, payload):
        pass

