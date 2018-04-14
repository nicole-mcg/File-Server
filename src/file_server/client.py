import socket, time, json
from collections import deque

from file_server.util.byte_buffer import ByteBuffer
from file_server.easy_socket import FileSocket
from file_server.file.packet.impl.idle import IdlePacket
from file_server.util import send_post_request
from file_server.web.account import Account

from .hub import Hub

class Client(Hub):
    TIMEOUT_INTERVALS = [2, 5, 5, 5, 10, 10, 30]
    IDLE_TIME = 1

    def __init__(self, directory, address, username, password):

        super(self.__class__, self).__init__(directory, FileSocket.PORT)

        self.directory = directory
        self.address = address
        self.host = socket.gethostname()
        self.packet_queue = deque()
        self.connected = False
        self.timeout_count = 0
        self.last_attempt = time.time()
        self.sock = None

        # Unused but collected because of client/server code mix...
        self.data_recieved = 0
        self.files_recieved = 0
        self.data_sent = 0
        self.files_sent = 0

        self.username = username
        self.password = password

    def validate(self):
        account = self.account = None

        request = send_post_request("http://" + self.address + ":8080/api/login", {
            "name": self.username,
            "password": self.password
        })

        if (request is None):
            print("Could not validate with current credentials.")
            return False

        print("Successfully created session")

        data = json.loads(request)

        account = Account(self.username, data["auth_code"], data["settings"]);
        account.session = data["session"]

        self.account = account
        return True

    def connect(self):

        print("Trying to connect to {}".format(self.address))

        if not self.validate():
            return

        try:
            timeout = Client.TIMEOUT_INTERVALS[self.timeout_count]
            while (time.time() - self.last_attempt <= timeout):
                time.sleep(0.5)
            self.sock = FileSocket(self, None, self.account.session)
            self.sock.sock.connect((self.host, FileSocket.PORT))

            self.sock.sock.send(ByteBuffer.from_int(len(self.account.session) + 1).bytes())
            self.sock.sock.send(ByteBuffer.from_string(self.account.session).bytes())

            b = ByteBuffer(self.sock.sock.recv(1)).read()

            if b == 0:
                print("Could not authenticate with server")
                return

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
                self.prepare_packets(self)

                # Send an idle packet if queue is empty and enough time has passed
                if (len(self.packet_queue) == 0 and time.time() - last_ping >= Client.IDLE_TIME):
                    self.packet_queue.append(IdlePacket())

                has_packet = not len(self.packet_queue) == 0

            
                # Send all packets in queue
                while (not len(self.packet_queue) == 0):
                    self.sock.send_packet(self.packet_queue.pop())
                    self.sock.send(ByteBuffer.from_bool(not len(self.packet_queue) == 0))

                # Read all incoming packets
                if (has_packet):
                    while (self.sock.read().read_bool()):
                        with self.sock.read_packet(): pass

                    last_ping = time.time()

            except ConnectionResetError as e:
                print(e)
                break

            time.sleep(Client.IDLE_TIME)
            

    def start(self):

        self.file_event_handler.sock = None

        while self.sock == None:
            self.connect()
            time.sleep(0.1)

        self.file_event_handler.sock = self.sock.sock

        while 1:
            if (self.connected):
                self.process()
                self.connected = False
                print("Connection to the server has been lost.")
            self.connect()

    def send_packet(self, packet):
        self.packet_queue.append(packet)