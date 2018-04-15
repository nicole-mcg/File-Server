import socket, contextlib, os

from file_server.util.byte_buffer import ByteBuffer
from file_server.file.packet.packet_manager import handle_incoming_packet
from file_server.file.packet.impl.idle import IdlePacket
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
    def __init__(self, hub, sock, session=None):
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
    def send(self, byte_buffer):

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
        buff.write_int(packet.size())

        # Check if we have a session to send (client)
        if self.session is not None:

            # Send session string
            buff.write_int(len(self.session) + 1)
            buff.write_string(self.session)

        else:

            # Send 0 for length of session string
            buff.write_int(0)

        # Send the buffer on the connection
        self.sock.send(buff.bytes())

        # Get the authentication response
        auth_response = ByteBuffer(self.sock.recv(1))
        authenticated = auth_response.read_bool()

        # Return if we aren't authenticated
        if not authenticated:
            print("Invalid server session")
            return

        # Use to packet handler to send the packet
        packet.handle_outgoing(self.hub, self)

        # Get response
        buff = ByteBuffer(self.sock.recv(4))
        length = buff.read_int()

        # Use packet handler for response
        packet.handle_response(ByteBuffer(self.sock.recv(length)))

    # Reads and handles a packet from the connection
    @contextlib.contextmanager
    def read_packet(self):

        # Read 5 bytes from stream (id and length)
        b = self.sock.recv(5)
        buff = ByteBuffer(b)

        # read_packet will wait at "self.sock.recv" above until data is available to be read
        # this yield allows functions to be performed before incoming packets are handled
        yield

        # Read ID and size
        id = buff.read()
        length = buff.read_int()

        # Get session length
        buff = ByteBuffer(self.sock.recv(4))
        session_length = buff.read_int()

        # Create response to authentication
        authenticated = False
        if (session_length > 0):

            # Check if provided session is valid and respond accordingly
            session = ByteBuffer(self.sock.recv(session_length)).read_string()
            if Account.is_valid_session(session):
                authenticated = True
        else:

            # No session provided, 
            authenticated = not self.needs_auth

        # Send auth response
        auth_response = ByteBuffer()
        auth_response.write_bool(authenticated)
        self.sock.send(auth_response.bytes())

        # Return if authentication was incorrect
        if not authenticated:
            return

        # Generate response using packet handler
        response = handle_incoming_packet(id, self.hub, self, length)

        # Send response if exists
        buff = ByteBuffer()
        if (response != None):
            buff.write_int(len(response))
            buff.write(response.bytes())
        else:
            buff.write_int(0)
        self.sock.send(buff.bytes())

    def send_file(self, file_name):
        sock = self.sock
        hub = self.hub
        directory = self.hub.directory

        file_size = get_file_size(self.hub.directory + file_name)

        sock.send(ByteBuffer.from_int(file_size).bytes())
        sock.send(ByteBuffer.from_string(file_name).bytes())

        hub.transferring = {
            "direction": "send",
            "file_name": file_name,
            "file_size": file_size
        }

        hub.transfer_progress = 0
        with open(directory + file_name, mode='rb') as file:

            while(file_size > 0):
                chunk_size = FileSocket.KILOBYTE if file_size > FileSocket.KILOBYTE else file_size
                chunk = file.read(chunk_size)
                sock.send(chunk)
                hub.data_sent += chunk_size
                hub.transfer_progress += chunk_size
                file_size -= chunk_size

        hub.files_sent += 1
        hub.transferring = None

    def save_file(self, packet_length):
        sock = self.sock
        hub = self.hub
        directory = hub.directory
        file_event_handler = hub.file_event_handler

        file_size = ByteBuffer(sock.recv(4)).read_int()
        packet_length -= 4

        name_length = packet_length - file_size
        file_name = ByteBuffer(sock.recv(name_length)).read_string()
        packet_length -= name_length

        file_path = directory + file_name
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        hub.transferring = {
            "direction": "recieve",
            "file_name": file_name,
            "file_size": file_size
        }

        if not os.path.isfile(file_path):
            file_event_handler.add_ignore(("change", file_name))
                
        file = open(file_path,'wb')

        hub.transfer_progress = 0
        while(packet_length > 0):
            file_event_handler.add_ignore(("change", file_name))
            chunk_size = FileSocket.KILOBYTE if packet_length > FileSocket.KILOBYTE else packet_length
            file.write(ByteBuffer(sock.recv(chunk_size)).bytes())
            file.flush()
            hub.transfer_progress += chunk_size
            hub.data_recieved += chunk_size
            packet_length -= chunk_size

        hub.files_recieved += 1
        hub.transferring = None

        file_event_handler.add_ignore(("change", file_name))
        file.close()