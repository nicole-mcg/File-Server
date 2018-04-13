import os, sys, socket, time
from threading import Thread

# Starts a client/server
def start_hub(hub_type, file_processor):

    if (hub_type is "server"): # Server

        from file_server.io.server import Server
        packet_queue = Server(file_processor)

        # Start webserver
        from file_server.web.webserver import create_webserver

        packet_queue.webserver = create_webserver(packet_queue)

        Thread(target = packet_queue.webserver.serve_forever).start()

    elif (hub_type is "client"): # Client

        try:
            from file_server.io.client import Client
            packet_queue = Client(file_processor, sys.argv[2], sys.argv[3], sys.argv[4])
        except LookupError: 
            print(username + " " + password)
            print("Invalid username or password")
            return

    else:

        print("Invalid hub type specified: '{}'. Should be 'server' or 'client'.")
        return #FIXME should throw error

    file_processor.initialize(packet_queue)

    packet_queue.start()

    file_processor.shutdown()