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
    # file_sock: the file_socket associated with the hub
    # length: the length of the packet
    # kwargs: exclusively for sending packets, sets properties in class for use later
    def __init__(self, hub=None, file_sock=None, length=0,**kwargs):
        self.file_sock = file_sock
        self.length = length
        self.hub = hub

        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def size(self):
        return 0;

    # Populates the payload for an outgoing packet
    def create_payload(self):
        return None

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

    # Returns the payload
    def get_payload(self):
        return self._payload
        