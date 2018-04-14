import sys
from threading import Thread

from file_server.file.packet.packet_manager import initialize_packet_manager

def start_hub():

    # Check if this is supposed to be a server or client based on number of args entered
    isServer = len(sys.argv) <= 2

    # Get directory to sync
    directory = sys.argv[1]

    # Create the hub
    if isServer:

        from .server import FileServer
        from .web.webserver import create_webserver

        # Use FileServer class for hub
        try: 
            hub = FileServer(directory)
        except OSError:
            print("File server could not be started")
            return

        # Start the webserver
        try:
            hub.webserver = create_webserver(hub)
            Thread(target = hub.webserver.serve_forever).start()
        except OSError:
            print("File server could not be started")
            server.kill()
            return

    else:

        from .client import Client

        # Use Client class for hub
        try:
            hub = Client(directory, sys.argv[2], sys.argv[3], sys.argv[4])
        except LookupError: # Couldn't authenticate 
            print("Invalid username or password")
            return

    initialize_packet_manager()

    hub.initialize()

    hub.start()

    hub.kill()

if __name__ == "__main__":

    # Make sure args length is correct
    if (len(sys.argv) <= 1):
        print("Command arguments should be in the form \"directory hostname user password\". Only directory is needed for server")
        sys.exit()

    start_hub()