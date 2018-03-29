
# from file_server.packet.impl import IdlePacket

packet_handlers = {}

def register_packet(cls):
    packet_handlers[cls.id] = cls

def handle_incoming_packet(id, sock, length, processor, conn=None):
    try:
        cls = packet_handlers[id]
    except:
        #TODO throw an error
        print("No handler found for ID: " + str(id))
        return None

    if (cls is not None):
        handler = cls(processor, sock, length, conn)
        if id is not 0:
            print("Handling packet: " + cls.name)
        return handler.handle_incoming()