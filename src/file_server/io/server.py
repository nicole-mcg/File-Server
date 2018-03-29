import socket
from collections import deque
from threading import Thread

from file_server.io import ByteBuffer

from .easy_socket import EasySocket 

from time import time

class Server:
    def __init__(self, hub_processor):
        self.hub_processor = hub_processor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

        hub_processor.update_status = True

    def start(self):
        self.sock.bind((socket.gethostname(), EasySocket.PORT))
        self.sock.listen(5)
        print("Waiting for connections on " + str(socket.gethostname()))
        while 1:
            clientsocket, address = self.sock.accept()
            print("Connection recieved: " + clientsocket.getpeername()[0])
            connection = ServerConnection(
                clientsocket.getpeername()[0],
                EasySocket(self.hub_processor, clientsocket),
                self.hub_processor,
                self
            )
            self.connections.append(connection)
            connection.start()

    def queue_packet(self, packet):
        for conn in self.connections:
            conn.queue_packet(packet)

class ServerConnection(Thread):
    def __init__(self, name, socket, hub_processor, server):
        super().__init__()
        self.client_host = name
        self.sock = socket
        self.hub_processor = hub_processor
        self.server = server
        self.packet_queue = deque()
        self.shutdown = False
        self.connect_time = time()
        self.data_recieved = 0
        self.files_recieved = 0
        self.data_sent = 0
        self.files_sent = 0
        self.transferring = None
        self.transfer_progress = 0

    def run(self):
        while (not self.shutdown):
            try: 
                # Wait for a packet
                with self.sock.read_packet(self):
                    self.hub_processor.pre(self)
                
                while self.sock.read().read_bool(): # Handle the rest of the packets
                    with self.sock.read_packet(self):
                        pass

                self.hub_processor.process(self)

                self.sock.send(ByteBuffer.from_bool(not len(self.packet_queue) == 0))
                while not len(self.packet_queue) == 0:
                    self.sock.send_packet(self.packet_queue.pop(), self)
                    self.sock.send(ByteBuffer.from_bool(not len(self.packet_queue) == 0))

                self.hub_processor.post(self)
            except ConnectionResetError as e:
                print(e)
                break

        print("Connection to client \"{}\" has been lost".format(self.client_host))

        connections = self.server.connections
        for i in range(len(connections)):
            if connections[i] is self:
                del connections[i]


    def queue_packet(self, packet):
        self.packet_queue.append(packet)

