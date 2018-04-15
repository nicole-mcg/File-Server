import requests, json, time, inspect
from threading import Thread

from file_server.server import FileServer
from file_server.file.file_socket import FileSocket
from file_server.hub.packet_manager import initialize_packet_manager
from file_server.web.webserver import create_webserver
from file_server.account.account_manager import set_account_manager_directory
from file_server.util import delete_file

# Starts a server on different ports using test directories
# auto_shutdown: the time (in seconds) before the server is automatically shut down
#                this might need to be changed for longer tests
def start_test_server(auto_shutdown=5):

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
    set_account_manager_directory(bin_path + "/")

    # Try to create the server
    try:
        server = FileServer(serv_dir, 8088)
    except OSError:
        assert False, "Another test server is already running"
        return

    # Starts the server on a new thread
    def start_server():

        server.webserver = create_webserver(server, 8081)

        # Start webserver
        Thread(target=server.webserver.serve_forever).start()

        initialize_packet_manager()

        # Initialize file watch
        server.initialize()

        # Start file server
        server.serve()

        # Shutdown file watch after server is shut down
        server.kill()

        return server

    # Used to kill the test server automatically if it's left running
    def kill_server():
        start = time.time()

        # Wait until auto shutdown time is reached
        while(time.time() < start + auto_shutdown):

            # Stop waiting if the server is already shut down
            if server.shutdown:
                return

            # Wait 500ms
            time.sleep(0.5)

        # Make sure the server isn't already shut down
        if not server.shutdown:

            # Kill the server
            server.kill()

            # Create an AssertionError because this is only a safety net
            assert False, "TEST \"{}\" DID NOT PROPERLY KILL SERVER. FAILSAFE TEST SERVER SHUTDOWN USED.".format(test_name)

    # Try to open the file server connection
    try:
        server.start(False)
    except OSError as e:

        # Kill anything the server was able to start
        server.kill()

        assert False, "Another test server is already running."
        return

    # Start the server on a new thread so the test can keep running
    thread = Thread(target=start_server)
    thread.start()

    # Start the auto shutdown on a new thread
    Thread(target=kill_server, args=[server, auto_shutdown, test_name]).start()

    return server

# Used to easily send a post request to a test server endpoint
# endpoint: the endpoint to send a request to (E.g endpoint="login")
# data: Any data to send along with the api request. This is turned into JSON
# session: The session for the request (for endpoints that require login)
def send_test_api_request(endpoint, data={}, session=""):

    # Send the request
    r = requests.post("http://127.0.0.1:8081/api/{}".format(endpoint), data=json.dumps(data), cookies={"session": session})

    # Check if the request was successfuly
    if r.status_code == 200:
        return r.text

    # Request wasn't successful
    return None