import os, sys, socket, time
from threading import Thread
from file_server.file.file_processor import FileProcessor

def start_hub():

    # Check if this is supposed to be a server or client based on number of args entered
    isServer = len(sys.argv) <= 2

    # Get directory to sync and create a file_processor instance
    directory = sys.argv[1]
    file_processor = FileProcessor(directory)

    # Create the hub
    if isServer:

        from file_server.io.server import FileServer
        from file_server.web.webserver import create_webserver

        # Use FileServer class for hub
        try: 
            hub = FileServer(directory, file_processor)
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

        from file_server.io.client import Client

        # Use Client class for hub
        try:
            hub = Client(directory, file_processor, sys.argv[2], sys.argv[3], sys.argv[4])
        except LookupError: # Couldn't authenticate 
            print("Invalid username or password")
            return

    file_processor.initialize(hub)

    hub.start()

    file_processor.shutdown()

if __name__ == "__main__":

    # Make sure args length is correct
    if (len(sys.argv) <= 1):
        print("Command arguments should be in the form \"directory hostname user password\". Only directory is needed for server")
        sys.exit()

    start_hub()