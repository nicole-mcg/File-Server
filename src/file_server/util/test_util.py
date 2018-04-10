
from threading import Thread
import os, shutil

from file_server.file.file_processor import FileProcessor
from file_server.io.server import Server
from file_server.web.webserver import create_webserver
from file_server.web.account import Account

from file_server.util import nuke_dir

# curr_directory should be the current directory for the python test file
#
# Get this with:
#   import os, inspect
#   curr_path = os.path.split(inspect.stack()[0][1])[0]
def start_test_server(curr_directory):

    bin_path = curr_directory + "/bin"
    if os.path.isdir(bin_path):
        nuke_dir(bin_path)

    serv_dir = bin_path + "/serv_dir/"

    os.makedirs(serv_dir, exist_ok=True)

    Account.directory = bin_path + "/"

    hub_processor = FileProcessor(serv_dir)
    packet_queue = Server(hub_processor, 8888)

    def start_server():

        packet_queue.webserver = create_webserver(packet_queue, 8081)

        # Start webserver
        Thread(target = packet_queue.webserver.serve_forever).start()

        hub_processor.initialize(packet_queue)

        packet_queue.start()

        hub_processor.shutdown()

        return packet_queue

    thread = Thread(target = start_server)

    thread.start()

    return packet_queue