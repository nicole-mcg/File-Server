import os, sys, socket, time
from threading import Thread

from .hub_processor import HubProcessor

# Starts a client/server
def start_hub(hub_type, hub_processor):

    if (hub_type is "server"): # Server

        from file_server.io.server import Server
        packet_queue = Server(hub_processor)

        # Start webserver
        from file_server.web.webserver import start_webserver
        Thread(target = start_webserver, args = [packet_queue]).start()

    elif (hub_type is "client"): # Client

        from file_server.io.client import Client
        packet_queue = Client(hub_processor, sys.argv[2])

    else:

        print("Invalid hub type specified: '{}'. Should be 'server' or 'client'.")
        return #FIXME should throw error

    hub_processor.initialize(packet_queue)

    packet_queue.start()

    hub_processor.shutdown()