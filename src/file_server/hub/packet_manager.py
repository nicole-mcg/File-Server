from file_server.hub.packets.idle import IdlePacket
from file_server.hub.packets.file_change import FileChangePacket
from file_server.hub.packets.file_add import FileAddPacket
from file_server.hub.packets.file_delete import FileDeletePacket
from file_server.hub.packets.file_move import FileMovePacket

# The dict of registered packet handlers
# This is used to get a handler for incoming packets
packet_handlers = {}

# Registers packet handlers for incoming packets
def initialize_packet_manager():

    def register_packet(cls):
        packet_handlers[cls.id] = cls

    register_packet(IdlePacket) # 0
    register_packet(FileChangePacket) # 1
    register_packet(FileAddPacket) # 2
    register_packet(FileDeletePacket) # 3
    register_packet(FileMovePacket) # 4

# Finds the appropriate packet handler and handles the incoming packet
# id: the ID of the packet
# hub: the hub associated with the incoming packet
def handle_incoming_packet(id, hub):

    # Try to find the packet handler
    try:
        cls = packet_handlers[id]
    except:
        print("No handler found for ID: " + str(id))
        return None

    # Make sure the handler we found is valid
    if (cls is not None):

        # Create the Packet instance
        handler = cls(hub)

        # Don't print for idle packets
        if id is not 0:
            print("Handling packet: " + cls.name)

        # handle the packet
        return handler.handle_incoming()