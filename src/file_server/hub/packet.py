from file_server.util.byte_buffer import ByteBuffer

# This class is used to handle packet protocol
class Packet:

    # List of registered packets
    # Used for incoming packets
    packet_handlers = {}

    # Name and id should be set in child classes
    name = "Packet"
    id = -1

    # hub: the FileHub associated with this packet
    # kwargs: exclusively for outgoing packets, sets properties in class for use later
    def __init__(self, hub=None, **kwargs):
        self.hub = hub

        self.file_sock = hub.file_sock if hub != None else None

        # Set class properties from kwargs
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    # Handles an outgoing packet
    def handle_outgoing(self, hub, file_sock):
        pass

    # Handles an incoming packet
    # Should return ByteBuffer or None
    def handle_incoming(self):
        pass

    # Handles an outgoing packet
    # This should be used to handle responses of outgoing paackets
    def handle_response(self, payload):
        pass
        