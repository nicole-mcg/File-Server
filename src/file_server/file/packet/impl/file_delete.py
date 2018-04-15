from file_server.file.packet.packet import Packet
from file_server.util.byte_buffer import ByteBuffer
from file_server.util import delete_file

class FileDeletePacket(Packet):
    name = "FileDeletePacket"
    id = 3
    def __init__(self, hub=None, file_sock=None, length=0, **kwargs):
        Packet.__init__(self, hub, file_sock, length)
        
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]

    def size(self):
        return len(self.file_name) + 5;

    def handle_outgoing(self, hub, file_sock):
        file_sock.sock.send(ByteBuffer.from_string(self.file_name).bytes())

    def handle_incoming(self):

        buff = ByteBuffer(self.file_sock.sock.recv(self.length)) if self.length > 0 else None
        file_name = buff.read_string()

        self.hub.file_event_handler.add_ignore(("delete", file_name))

        delete_file(self.hub.directory + file_name)

    def handle_response(self, payload):
        pass

