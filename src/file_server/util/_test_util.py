import pytest

import shutil, requests, json, time, inspect

from file_server.file.file_processor import FileProcessor
from file_server.io.server import Server
from file_server.web.webserver import create_webserver
from file_server.web.account import Account

from file_server.util import delete_file


#FIXME remove this
import webbrowser

import os, sys, socket, time
from threading import Thread
from file_server.file.file_processor import FileProcessor
from file_server.io.easy_socket import EasySocket

# Starts a server on different ports using test directories
def start_test_server(auto_shutdown=5):

    # webbrowser.open("http://test server started.com", new=2)

    # Get info for test being run
    test_path = os.path.split(inspect.stack()[1][1])
    curr_directory = test_path[0]
    test_name = test_path[1]

    # Create a temp "bin" folder and delete old one if it exists
    bin_path = curr_directory + "/bin"
    if os.path.isdir(bin_path):
        try:
            delete_file(bin_path)
        except OSError as e:
            print(e)
            assert False, "Another test is currently using this directory. {}".format(test_name)
            return

    # Create a directory for the file server
    serv_dir = bin_path + "/serv_dir/"
    os.makedirs(serv_dir, exist_ok=True)

    # Mark the directory for storing account info
    Account.directory = bin_path + "/"

    # Create test server
    file_processor = FileProcessor(serv_dir)

    server = None
    try:
        server = Server(file_processor, 8088)
    except OSError:
        assert False, "Another test server is already running"
        return

    # Starts the server on a new thread
    def start_server():

        server.webserver = create_webserver(server, 8081)

        # Start webserver
        Thread(target=server.webserver.serve_forever).start()

        # Initialize file watch
        file_processor.initialize(server)

        # Start file server
        server.serve()

        # Shutdown file watch after server is shut down
        file_processor.shutdown()

        return server

    # Used to kill the test server automatically if it's left running
    def kill_server():
        start = time.time()

        while(time.time() < start + auto_shutdown):
            if server.shutdown:
                return
            time.sleep(0.5)

        if not server.shutdown:
            server.kill()
            assert False, "TEST \"{}\" DID NOT PROPERLY KILL SERVER. FAILSAFE TEST SERVER SHUTDOWN USED.".format(test_name)

    # Open the file server connection
    try:
        server.start(False)
    except OSError as e:
        # print(e)
        server.kill()
        assert False, "Another test server is already running."
        return

    thread = Thread(target=start_server)

    thread.start()

    Thread(target=kill_server, args=[server, auto_shutdown, test_name]).start()

    return server

# endpoint should be a string
def send_test_api_request(endpoint, data={}, session=""):
    r = requests.post("http://127.0.0.1:8081/api/{}".format(endpoint), data=json.dumps(data), cookies={"session": session})

    if r.status_code == 200:
        return r.text

    return None