from file_server.packet import Packet
from file_server.io import ByteBuffer

class FileAddPacket(Packet):
    name = "FileAddPacket"
    id = 2
    def __init__(self, payload=None, **kwargs):
        if "file_name" in kwargs and "file_contents" in kwargs:
            buff = ByteBuffer.from_string(kwargs["file_name"])
            buff.write_int(len(kwargs["file_contents"]))
            buff.write(kwargs["file_contents"])
            payload = buff.bytes()
        super(self.__class__, self).__init__(payload)
        self.payload = payload


    def handle_incoming(self, hub_processor):
        buff = self.payload
        file_name = buff.read_string()
        
        length = buff.read_int()

        b = bytearray()
        for i in range(length):
            b.append(buff.read())

        hub_processor.create_file(file_name, bytes(b))

    def handle_response(self, payload):
        pass

