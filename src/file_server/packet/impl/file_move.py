from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileMovePacket(Packet):
    name = "FileDeletePacket"
    id = 4
    def __init__(self, payload=None, **kwargs):
        if "file_name" in kwargs:
            buff = ByteBuffer.from_string(kwargs["file_name"])
            buff.write_string(kwargs["new_name"])
            payload = buff.bytes()
        super(self.__class__, self).__init__(payload)
        self.payload = payload

    def handle_incoming(self, hub_processor):
        buff = self.payload
        file_name = buff.read_string()
        new_name = buff.read_string()

        hub_processor.move_file(file_name, new_name)

    def handle_response(self, payload):
        pass

