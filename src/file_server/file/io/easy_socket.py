import socket, contextlib, os

from file_server.file.io.byte_buffer import ByteBuffer
from file_server.file.packet import handle_incoming_packet
from file_server.file.packet.impl.idle import IdlePacket
from file_server.web.account import Account
from file_server.util import get_file_size


class EasySocket:
    KILOBYTE = 1024
    PORT = 1234

    def __init__(self, hub, sock, session=None):
        self.hub = hub
        self.session = session
        self.needs_auth = self.session is None

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def send(self, byte_buffer):
        self.sock.send(ByteBuffer.from_int(len(byte_buffer)).bytes())
        self.sock.send(byte_buffer.bytes())

    def read(self):
        b = self.sock.recv(4)
        length = ByteBuffer(b).read_int()
        return ByteBuffer(self.sock.recv(length))

    def send_packet(self, packet=None):

        if packet is None:
            packet = IdlePacket()

        if not hasattr(packet.__class__, "name"):
            import pdb; pdb.set_trace();

        print("Sending packet: {}".format(packet.__class__.name))
        buff = ByteBuffer()

        # Send ID and size
        buff.write(packet.__class__.id)
        buff.write_int(packet.size())

        if self.session is not None:
            buff.write_int(len(self.session) + 1)
            buff.write_string(self.session)
        else:
            buff.write_int(0)

        self.sock.send(buff.bytes())

        
        auth_response = ByteBuffer(self.sock.recv(1))

        b = auth_response.read()
        if b == 0:
            print("invalid client authentification")
            return

        #packet sock is not set at the time of writing this
        packet.handle_outgoing(self.hub, self)

        # Handle response
        buff = ByteBuffer(self.sock.recv(4))
        length = buff.read_int()
        packet.handle_response(ByteBuffer(self.sock.recv(length)))

    @contextlib.contextmanager
    def read_packet(self):
        b = self.sock.recv(5)
        buff = ByteBuffer(b)

        yield

        # Read ID and size
        id = buff.read()
        length = buff.read_int()

        buff = ByteBuffer(self.sock.recv(4))
        auth_length = buff.read_int()

        auth_response = ByteBuffer()
        if (auth_length > 0):
            auth = ByteBuffer(self.sock.recv(auth_length)).read_string()
            if not Account.is_valid_session(auth):
                auth_response.write(0)
            else:
                auth_response.write(1)
        else:
            auth_response.write(1 if not self.needs_auth else 0)

        self.sock.send(auth_response.bytes())

        # Generate response
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
                chunk_size = EasySocket.KILOBYTE if file_size > EasySocket.KILOBYTE else file_size
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
            chunk_size = EasySocket.KILOBYTE if packet_length > EasySocket.KILOBYTE else packet_length
            file.write(ByteBuffer(sock.recv(chunk_size)).bytes())
            file.flush()
            hub.transfer_progress += chunk_size
            hub.data_recieved += chunk_size
            packet_length -= chunk_size

        hub.files_recieved += 1
        hub.transferring = None

        file_event_handler.add_ignore(("change", file_name))
        file.close()