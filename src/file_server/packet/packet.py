from file_server.io import ByteBuffer

class Packet:
    name = "Packet"
    packet_handlers = {}

    def __init__(self, file_processor, easy_sock=None, length=0, hub=None):
        self.easy_sock = easy_sock
        self.length = length
        self.file_processor = file_processor
        self.hub = hub

    def size(self):
        return 0;

    # Populates the payload for an outgoing packet
    def create_payload(self):
        return None

    # Handles an outgoing packet
    def handle_outgoing(self, easy_sock, hub):
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
        