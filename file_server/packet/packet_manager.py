packet_handlers = {}

def register_packet(cls):
    packet_handlers[cls.id] = cls

def handle_incoming_packet(id, payload, processor):
    try:
        cls = packet_handlers[id]
    except:
        #TODO throw an error
        print("No handler found for ID: " + str(id))
        return None

    if (cls is not None):
        handler = cls(payload)
        print("Handling packet: " + cls.name)
        return handler.handle_incoming(processor)