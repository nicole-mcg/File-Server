from file_server.hub.packet import Packet
from file_server.util.byte_buffer import ByteBuffer
from file_server.util import delete_file

# Used to handle protocol for sending and recieving file deletion events
class FileDeletePacket(Packet):
    name = "FileDeletePacket"
    id = 3

    # hub: the FileHub associated with this packet
    # kwargs: exclusively for outgoing packets {
    #     file_name: name of deleted local file     
    # }
    def __init__(self, hub=None, **kwargs):
        Packet.__init__(self, hub, **kwargs)

    # Handles an outgoing packet
    def handle_outgoing(self, hub, file_sock):
        file_sock.write(ByteBuffer.from_string(self.file_name))

    # Handles an incoming packet
    def handle_incoming(self):

        buff = self.file_sock.read()
        file_name = buff.read_string()

        self.hub.file_event_handler.add_ignore(("delete", file_name))

        delete_file(self.hub.directory + file_name)