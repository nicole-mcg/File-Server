from threading import Thread

# This class represents a processor for the server/client
# It is the entry point for the program's logic
class HubProcessor:

    # Called right before incoming packets are handled
    def pre(self, packet_queue):
        pass

    # Called after incoming packets are handled
    def process(self, packet_queue):
        pass

    # Called 
    def post(self, packet_queue):
        pass