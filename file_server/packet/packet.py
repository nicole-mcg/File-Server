from file_server.io import ByteBuffer

class Packet:
    name = "Packet"
    packet_handlers = {}

    def __init__(self, payload=ByteBuffer()):
        self._payload = payload

    def __len__(self):
        return len(self._payload) if self._payload != None else 0

    # Populates the payload for an outgoing packet
    def create_payload(self):
        return None

    # Handles an incoming packet
    # Should return ByteBuffer or None
    def handle_incoming(self, hub_processor):
        pass

    # Handles an outgoing packet
    # This should be used to handle responses
    def handle_response(self, payload):
        pass

    # Returns the payload
    def get_payload(self):
        return self._payload
        