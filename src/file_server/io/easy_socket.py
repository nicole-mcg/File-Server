import socket, contextlib

from file_server.io import ByteBuffer
from file_server.packet import handle_incoming_packet
from file_server.packet.impl import IdlePacket

class EasySocket:
    PORT = 1234

    def __init__(self, hub_processor, sock=None):
        self.hub_processor = hub_processor
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

    def send_packet(self, packet=None, conn=None):

        if packet is None:
            packet = IdlePacket(self.hub_processor)

        if not hasattr(packet.__class__, "name"):
            import pdb; pdb.set_trace();

        print("Sending packet: {}".format(packet.__class__.name))
        buff = ByteBuffer()

        # Send ID and size
        buff.write(packet.__class__.id)
        buff.write_int(packet.size())

        self.sock.send(buff.bytes())

        #packet sock is not set at the time of writing this
        packet.handle_outgoing(self.sock, conn)

        # Handle response
        buff = ByteBuffer(self.sock.recv(4))
        length = buff.read_int()
        packet.handle_response(ByteBuffer(self.sock.recv(length)))

    @contextlib.contextmanager
    def read_packet(self, conn=None):
        b = self.sock.recv(5)
        buff = ByteBuffer(b)

        yield

        # Read ID and size
        id = buff.read()
        length = buff.read_int()

        # Generate response
        response = handle_incoming_packet(id, self.sock, length, self.hub_processor, conn)

        # Send response if exists
        buff = ByteBuffer()
        if (response != None):
            buff.write_int(len(response))
            buff.write(response.bytes())
        else:
            buff.write_int(0)
        self.sock.send(buff.bytes())