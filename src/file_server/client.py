import socket, time, json
from collections import deque

from file_server.util.byte_buffer import ByteBuffer
from file_server.file.file_socket import FileSocket
from file_server.hub.packets.idle import IdlePacket
from file_server.util import send_post_request
from file_server.account.account import Account

from .hub.file_hub import FileHub

# This class represents a client that can connect to a a FileServer
class FileClient(FileHub):

    # The time (in seconds) to wait after each retry
    # Will increase to next time after unsuccessful connect attempt
    # Retries indefinitely at last time
    TIMEOUT_INTERVALS = [2, 5, 5, 5, 10, 10, 30]

    # A packet must wait at least this time (in seconds) after being created, before being sent
    PACKET_IDLE_TIME = 1

    # directory: the directory to watch
    # address: the address of the server
    # username: the username to attempt authentication with
    # password: the password to attempt authentication with
    def __init__(self, directory, address, username, password):
        self.directory = directory
        self.address = address
        self.username = username
        self.password = password

        # Initialize parent class
        FileHub.__init__(self, directory, FileSocket.PORT)

        #FIXME I believe this is incorrect
        # It will cause issues when a server and client are used on different computers (it should work for testing atm..)
        self.host = socket.gethostname()

        # The queue for packets ready to be sent
        self.packet_queue = deque()

        # Marks client for shutdown when possible
        self.shutdown = False

        # True when the client has an active connection to the server
        self.connected = False

        # The current index for TIMEOUT_INTERVALS
        self.timeout_count = 0

        # The time the last connection attempt was made
        self.last_attempt = time.time()

        # type: FileSocket
        # The socket used to talk to the server
        self.file_sock = None

        # Unused but collected because of client/server code mix...
        self.data_recieved = 0
        self.files_recieved = 0
        self.data_sent = 0
        self.files_sent = 0

    # Used to completely kill the client
    def kill(self):

        # Call kill in parent class
        FileHub.kill(self)

        # Mark for shutdown when possible
        self.shutdown = True
        self.connected = False

        # Close the connection
        self.file_sock.sock.close()

    # Get a valid session ID from the webserver
    def validate(self):
        account = self.account = None

        # Send the login request
        request = send_post_request("http://" + self.address + ":8080/api/login", {
            "name": self.username,
            "password": self.password
        })

        # Could not connect to the server
        if request is None:
            print("Could not connect to server.")
            return False

        # turn the response into a usable object
        data = json.loads(request)

        # Invalid credentials
        if "error" in data:
            print("Could not authenticate with server: ".format(data["error"]))
            return False

        # Create an account object to hold the info
        account = Account(self.username, data["auth_code"], data["settings"]);
        account.session = data["session"]
        self.account = account

        return True

    # Attempt to connect (or reconnect) to the server
    def connect(self):

        print("Trying to connect to {}".format(self.address))

        # Try to create a session with the server
        if not self.validate():
            return

        try:

            # Time to wait (in seconds)
            timeout = FileClient.TIMEOUT_INTERVALS[self.timeout_count]

            # Wait until the time has passed
            while (time.time() - self.last_attempt <= timeout):
                time.sleep(0.5)

            # Create socket and connect to server
            self.file_sock = FileSocket(None, self, self.account.session)
            self.file_sock.sock.connect((self.host, FileSocket.PORT))

            # Send the session key
            self.file_sock.write(ByteBuffer.from_string(self.account.session))

            # Check the validation response
            authenticated = self.file_sock.read().read_bool()

            # Server didn't think our session was valid
            if not authenticated:
                print("Could not authenticate with server")
                return

            # Reset reconnect variables
            self.last_attempt = 0
            self.timeout_count = 0

            # Mark client as connected
            self.connected = True

            print("Successfully connected")

        except (ConnectionRefusedError, socket.timeout):
            # The connection wasn't accepted...

            # Set the time of last attempt to current time
            self.last_attempt = time.time()

            # Time to wait (in seconds)
            timeout = FileClient.TIMEOUT_INTERVALS[self.timeout_count]

            print("Could not connect to server. Trying again in {} seconds".format(timeout))

            # Move to the next wait time if possible
            if self.timeout_count < len(FileClient.TIMEOUT_INTERVALS) - 1:
                self.timeout_count += 1

    # Processes the active connection until it's lost
    def process(self):

        # The last time we've spoken to the server
        last_ping = 0

        while self.connected:#This should listen for file and server changes

            try:

                # Process packets in the buffer queue
                self.prepare_packets(self)

                # Send an idle packet if queue is empty and enough time has passed
                if (len(self.packet_queue) == 0 and time.time() - last_ping >= FileClient.PACKET_IDLE_TIME):
                    self.packet_queue.append(IdlePacket())

                # Check if we're sending any packets so we can still know after they're sent
                has_packet = not len(self.packet_queue) == 0
            
                # Send all packets in queue
                while not len(self.packet_queue) == 0:
                    self.file_sock.send_packet(self.packet_queue.pop())
                    self.file_sock.write(ByteBuffer.from_bool(not len(self.packet_queue) == 0))

                # Server will only respond if we actually sent something
                if has_packet:

                    # Read all packets from the server
                    while (self.file_sock.read().read_bool()):
                        with self.file_sock.read_packet(): pass

                    # Set the last time we spoke to the server to the current time
                    last_ping = time.time()

            except ConnectionResetError as e:
                # We've lost connection to the server
                self.connected = False
                print(e)
                break

            # Wait for a fourth of the PACKET_IDLE_TIME
            # This is to save system resources while still frequently updating if needed
            time.sleep(FileClient.PACKET_IDLE_TIME / 4)
            
    # Runs the client connection on the current thread
    def start(self):

        # Try to connect until it works
        while self.file_sock == None:
            self.connect()
            time.sleep(0.1)

        # Keep trying to reconnect until shutdown
        while not self.shutdown:

            # Start processing the connection if we're already connected
            if (self.connected):

                # Process the connection until it is lost
                self.process()

                # Mark that we're not connected
                self.connected = False

                print("Connection to the server has been lost.")

            # Try to connect
            self.connect()

    # Queues a packet to be sent on the connection
    # packet: the Packet to be sent
    def send_packet(self, packet):
        self.packet_queue.append(packet)