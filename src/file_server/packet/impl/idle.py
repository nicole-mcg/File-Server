from file_server.packet import Packet

class IdlePacket(Packet):
    name = "IdlePacket"
    id = 0

    def handle_outgoing(self, easy_sock, hub):
        pass

    def handle_incoming(self):
        pass

    def handle_response(self, payload):
        pass