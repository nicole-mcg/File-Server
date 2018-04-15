from file_server.hub.packet import Packet

# An empty packet used to verify connection
class IdlePacket(Packet):
    name = "IdlePacket"
    id = 0