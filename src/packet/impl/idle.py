from file_server.packet import Packet

class IdlePacket(Packet):
    name = "IdlePacket"
    id = 0

    def handle_incoming(self, hub_processor):
        pass

    def handle_response(self, payload):
        pass