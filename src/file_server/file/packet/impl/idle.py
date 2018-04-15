from file_server.file.packet.packet import Packet

class IdlePacket(Packet):
    name = "IdlePacket"
    id = 0

    def handle_outgoing(self, hub, file_sock):
        pass

    def handle_incoming(self):
        pass

    def handle_response(self, payload):
        pass