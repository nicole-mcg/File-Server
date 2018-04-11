
from threading import Thread
import os, shutil, requests, json, time, inspect

from file_server.file.file_processor import FileProcessor
from file_server.io.server import Server
from file_server.web.webserver import create_webserver
from file_server.web.account import Account

from file_server.util import nuke_dir


#FIXME remove this
import webbrowser

# curr_directory should be the current directory for the python test file
#
# Get this with:
#   import os, inspect
#   curr_path = os.path.split(inspect.stack()[0][1])[0]
def start_test_server(auto_shutdown=5):

    test_path = os.path.split(inspect.stack()[1][1])
    curr_directory = test_path[0]
    test_name = test_path[1]

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
        Thread(target=packet_queue.webserver.serve_forever).start()

        hub_processor.initialize(packet_queue)

        packet_queue.start()

        hub_processor.shutdown()

        return packet_queue

    def kill_server(server, wait_time, test_name):
        start = time.time()
        while(time.time() < start + wait_time):
            time.sleep(0.5)
        server.kill()
        raise Exception("TEST \"{}\" DID NOT PROPERLY KILL SERVER. FAILSAFE TEST SERVER SHUTDOWN USED.".format(test_name))

    thread = Thread(target=start_server)

    thread.start()

    Thread(target=kill_server, args=[packet_queue, auto_shutdown, test_name]).start()

    return packet_queue

# endpoint should be a string
def send_api_request(endpoint, data={}, session=""):
    r = requests.post("http://127.0.0.1:8081/api/{}".format(endpoint), data=json.dumps(data), cookies={"session": session})

    if r.status_code == 200:
        return r.text

    return None