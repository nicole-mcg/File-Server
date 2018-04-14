from file_server.util.byte_buffer import ByteBuffer

class Packet:
    name = "Packet"
    packet_handlers = {}

    def __init__(self, hub=None, easy_sock=None, length=0):
        self.easy_sock = easy_sock
        self.length = length
        self.hub = hub

    def size(self):
        return 0;

    # Populates the payload for an outgoing packet
    def create_payload(self):
        return None

    # Handles an outgoing packet
    def handle_outgoing(self, hub, easy_sock):
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
        