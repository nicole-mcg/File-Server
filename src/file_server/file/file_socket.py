import socket, contextlib, os

from file_server.util.byte_buffer import ByteBuffer
from file_server.hub.packet_manager import handle_incoming_packet
from file_server.hub.packets.idle import IdlePacket
from file_server.web.account import Account
from file_server.util import get_file_size

# This class is used to handle common protocols on the server
class FileSocket:
    
    # The size of one kilobyte (in bytes). This is used to make intent more clear
    KILOBYTE = 1024

    # The default port for FileServer and FileClient
    PORT = 1234

    # hub: the FileServer or FileClient this socket is associated with
    # sock: the raw socket for the connection
    def __init__(self, sock, hub=None, session=None):
        self.hub = hub
        self.session = session

        # Marks whether sessions need to be authenticated for packets (this is for servers)
        self.needs_auth = self.session is None

        # Create a socket if none is given
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    # Converts a ByteBuffer to bytes and sends it on the connection
    # Handles length of data automatically
    # byte_buffer: the ByteBuffer to send
    def write(self, byte_buffer):

        # Send length of data
        self.sock.send(ByteBuffer.from_int(len(byte_buffer)).bytes())

        # Send data
        self.sock.send(byte_buffer.bytes())

    # Reads a ByteBuffer from the stream
    # Handles length of data automatically
    def read(self):

        # Get length of data
        length = ByteBuffer(self.sock.recv(4)).read_int()

        # Read data
        return ByteBuffer(self.sock.recv(length))

    # Sends a packet on the connection
    # packet: The packet to send. IdlePacket is used if no packet is specified
    def send_packet(self, packet=None):

        # Use IdlePacket if packet was specified
        if packet is None:
            packet = IdlePacket()

        print("Sending packet: {}".format(packet.__class__.name))

        buff = ByteBuffer()

        # Write packet ID and size
        buff.write(packet.__class__.id)

        # Check if we have a session to send (client)
        session = ""
        if self.session is not None:
            session = self.session

        buff.write_string(session)

        # Send the buffer on the connection
        self.write(buff)

        # Get the authentication response
        authenticated = ByteBuffer(self.sock.recv(1)).read_bool()

        # Return if we aren't authenticated
        if not authenticated:
            print("Invalid server session")
            return

        # Send packet using packet handler
        packet.handle_outgoing(self.hub, self)

    # Reads and handles a packet from the connection
    @contextlib.contextmanager
    def read_packet(self):

        # Read packet info into byte buffer
        buff = self.read()

        # this function will wait at "self.sock.recv" above until data is available to be read
        # this yield allows caller to perform actions before incoming packets are handled
        yield

        # Read ID and size
        id = buff.read()

        session = buff.read_string()

        # Create response to authentication
        authenticated = False
        if session == "":

            # No session provided
            authenticated = not self.needs_auth

        elif Account.is_valid_session(session):

            # Session is valid
            authenticated = True

        # Send auth response
        self.sock.send(ByteBuffer.from_bool(authenticated).bytes())

        # Return if authentication was incorrect
        if not authenticated:
            return

        # Handle packet using packet handler
        handle_incoming_packet(id, self.hub)

    # Sends a file on the connection
    # Updates the hub with transfer progress
    def send_file(self, file_name):
        hub = self.hub

        data_left = get_file_size(hub.directory + file_name)

        # Send file name and size
        buff = ByteBuffer.from_string(file_name)
        buff.write_int(data_left)
        self.write(buff)

        # Update hub transfer status
        hub.transferring = {
            "direction": "send",
            "file_name": file_name,
            "file_size": data_left
        }
        hub.transfer_progress = 0

        # Open file for reading
        file = open(hub.directory + file_name, mode='rb')

        # Keep sending file data until we've transferred the whole file
        while(data_left > 0):

            # determine chunk size
            chunk_size = FileSocket.KILOBYTE if data_left > FileSocket.KILOBYTE else data_left

            # Read chunk from file and send on connection
            self.sock.send(file.read(chunk_size))

            # Update hub transfer progress
            hub.data_sent += chunk_size
            hub.transfer_progress += chunk_size

            data_left -= chunk_size

        # Close file
        file.close()

        # Update hub transfer status
        hub.files_sent += 1
        hub.transferring = None

    # Recieved a file on the connection and saves it locally
    # Updates the hub with transfer progress
    def save_file(self):
        sock = self.sock
        hub = self.hub
        directory = hub.directory
        file_event_handler = hub.file_event_handler

        # Read file name and size
        buff = self.read()
        file_name = buff.read_string()
        data_left = buff.read_int() # File size

        file_path = directory + file_name

        # Create any directories that don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Update hub transfer status
        hub.transferring = {
            "direction": "recieve",
            "file_name": file_name,
            "file_size": data_left
        }
        hub.transfer_progress = 0

        # Add event ignore if the file is being created now
        if not os.path.isfile(file_path):
            file_event_handler.add_ignore(("change", file_name))
                
        # Open file for writing
        file = open(file_path,'wb')

        # Keep reading data until we've recieved the whole file
        while(data_left > 0):

            # Add file change event ignore to hub event handler
            file_event_handler.add_ignore(("change", file_name))

            # Determine hub size
            chunk_size = FileSocket.KILOBYTE if data_left > FileSocket.KILOBYTE else data_left

            # Read chunk from connection and write directly to file
            file.write(sock.recv(chunk_size))

            # Flush to force a file change event
            # This let's us make sure we're creating the correct number of ignores
            file.flush()

            # Update hub transfer progress
            hub.transfer_progress += chunk_size
            hub.data_recieved += chunk_size
            data_left -= chunk_size

        # Ignore event generated by file.close
        file_event_handler.add_ignore(("change", file_name))

        # Close file
        file.close()

        # Update hub transfer status
        hub.files_recieved += 1
        hub.transferring = None

        