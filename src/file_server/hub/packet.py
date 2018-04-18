from file_server.util.byte_buffer import ByteBuffer

# This class is used to handle packet protocol
class Packet:

    # Name and id should be set in child classes
    name = "Packet"
    id = -1

    # hub: the FileHub associated with this packet
    # kwargs: exclusively for outgoing packets, sets properties in class for use later
    def __init__(self, hub=None, **kwargs):
        self.hub = hub

        if hub != None and hasattr(hub, "file_sock"):
            self.file_sock = hub.file_sock
        else:
            self.file_sock = None

        # Set class properties from kwargs
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    # Handles an outgoing packet
    def handle_outgoing(self, hub, file_sock):
        pass

    # Handles an incoming packet
    def handle_incoming(self):
        pass