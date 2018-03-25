from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileDeletePacket(Packet):
    name = "FileDeletePacket"
    id = 3
    def __init__(self, payload=None, **kwargs):
        if "file_name" in kwargs:
            payload = ByteBuffer.from_string(kwargs["file_name"]).bytes()
        super(self.__class__, self).__init__(payload)
        self.payload = payload


    def handle_incoming(self, hub_processor):
        buff = self.payload
        file_name = buff.read_string()

        hub_processor.delete_file(file_name)

    def handle_response(self, payload):
        pass

