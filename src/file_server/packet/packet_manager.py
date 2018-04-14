
from file_server.packet.impl import IdlePacket, FileChangePacket, FileAddPacket, FileDeletePacket, FileMovePacket

packet_handlers = {}

def initialize_packet_manager():
    register_packet(IdlePacket) # 0
    register_packet(FileChangePacket) # 1
    register_packet(FileAddPacket) # 2
    register_packet(FileDeletePacket) # 3
    register_packet(FileMovePacket) # 4

def register_packet(cls):
    packet_handlers[cls.id] = cls

def handle_incoming_packet(id, hub, sock, length):
    try:
        cls = packet_handlers[id]
    except:
        #TODO throw an error
        print("No handler found for ID: " + str(id))
        return None

    if (cls is not None):
        handler = cls(hub, sock, length)
        if id is not 0:
            print("Handling packet: " + cls.name)
        return handler.handle_incoming()