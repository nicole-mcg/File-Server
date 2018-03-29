import socket, sys, time
from collections import deque

from file_server.packet.impl import IdlePacket
from file_server.io import ByteBuffer

from .easy_socket import EasySocket

class Client:
    TIMEOUT_INTERVALS = [2, 5, 5, 5, 10, 10, 30]
    IDLE_TIME = 1

    def __init__(self, hub_processor, host):
        self.hub_processor = hub_processor
        self.host = host if host != 'localhost' else socket.gethostname()
        self.packet_queue = deque()
        self.connected = False
        self.timeout_count = 0
        self.last_attempt = time.time()

        # Unused but collected because of client/server code mix...
        self.data_recieved = 0
        self.files_recieved = 0
        self.data_sent = 0
        self.files_sent = 0

    def connect(self):
        try:
            timeout = Client.TIMEOUT_INTERVALS[self.timeout_count]
            while (time.time() - self.last_attempt <= timeout):
                time.sleep(0.5)

            print("Trying to connect to {}".format(self.host))
            self.sock = EasySocket(self.hub_processor)
            self.sock.sock.connect((self.host, EasySocket.PORT))

            self.last_attempt = 0
            self.timeout_count = 0;
            self.connected = True
            print("Successfully connected")
        except (ConnectionRefusedError, socket.timeout):
            self.last_attempt = time.time()
            timeout = Client.TIMEOUT_INTERVALS[self.timeout_count]
            print("Could not connect to server. Trying again in {} seconds".format(timeout))
            if self.timeout_count < len(Client.TIMEOUT_INTERVALS) - 1:
                self.timeout_count += 1

    def process(self):
        last_ping = 0
        while self.connected:#This should listen for file and server changes

            try:
                self.hub_processor.pre(self)

                # Send an idle packet if queue is empty and enough time has passed
                if (len(self.packet_queue) == 0 and time.time() - last_ping >= Client.IDLE_TIME):
                    self.packet_queue.append(IdlePacket(None))

                has_packet = not len(self.packet_queue) == 0

            
                # Send all packets in queue
                while (not len(self.packet_queue) == 0):
                    self.sock.send_packet(self.packet_queue.pop(), self)
                    self.sock.send(ByteBuffer.from_bool(not len(self.packet_queue) == 0))

                

                # Read all incoming packets
                if (has_packet):
                    while (self.sock.read().read_bool()):
                        with self.sock.read_packet(self): pass
                    self.hub_processor.process(self)
                    last_ping = time.time()

                self.hub_processor.post(self)
            except ConnectionResetError as e:
                print(e)
                break

            time.sleep(Client.IDLE_TIME)
            

    def start(self):

        self.connect()

        self.hub_processor.event_handler.sock = self.sock.sock

        while 1:
            if (self.connected):
                self.process()
                self.connected = False
                print("Connection to the server has been lost.")
            self.connect()

    def queue_packet(self, packet):
        self.packet_queue.append(packet)