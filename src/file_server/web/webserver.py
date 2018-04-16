import os, json, webbrowser

from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

from file_server.account.account_manager import load_account_from_session

from .endpoints.active_clients import ActiveClientsEndpoint
from .endpoints.client_info import ClientInfoEndpoint
from .endpoints.login import LoginEndpoint
from .endpoints.logout import LogoutEndpoint
from .endpoints.signup import SignupEndpoint
from .endpoints.user import UserEndpoint
from .endpoints.createauth import CreateAuthEndpoint
from .endpoints.update_settings import UpdateSettingsEndpoint
from .endpoints.directory_contents import DirectoryContentsEndpoint

from file_server.util import send_post_request

def register_endpoint(endpoint_class):

    # Make sure the endpoint class has a PATH property
    if not hasattr(endpoint_class, "PATH"):
        raise AssertionError("Endpoint class does not have PATH attribute")

    # Add the endpoint class to the dict of handlers
    RequestHandler.endpoints[endpoint_class.PATH] = endpoint_class

def create_webserver(server, port=8080):
    webserver = ThreadedHTTPServer(server, port)

    os.chdir("../web")

    RequestHandler.endpoints = {}

    register_endpoint(ActiveClientsEndpoint)
    register_endpoint(ClientInfoEndpoint)
    register_endpoint(LoginEndpoint)
    register_endpoint(LogoutEndpoint)
    register_endpoint(SignupEndpoint)
    register_endpoint(UserEndpoint)
    register_endpoint(CreateAuthEndpoint)
    register_endpoint(UpdateSettingsEndpoint)
    register_endpoint(DirectoryContentsEndpoint)
    

    return webserver

# This class represents a multithreaded HTTP server that can be shut down
# ThreadingMixIn makes it multithreaded
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    # server: the FileServer this webserver is associated with
    # port: the port to listen on
    def __init__(self, server, port):
        HTTPServer.__init__(self, ('', port), RequestHandler)
        self.server = server
        self.port = port

        # Marks the server for shutdown when possible
        self.shutdown = False

    # Listens for connections until shutdown
    def serve_forever(self):

        # Open the web browser
        webbrowser.open('http://127.0.0.1:8080', new=2)

        # Handle requests until shutdown
        # Because of the nature of handle_request, shutdown will not happen until a request is made
        while not self.shutdown:
            self.handle_request()

    # Used to comepletely kill the web server
    def kill(self):
        self.server_close()
        self.shutdown = True
        self._create_dummy_request()

    # Creates a dummy request
    # Used to ensure shutdown
    def _create_dummy_request(self):
        send_post_request("http://127.0.0.1:{}/".format(self.port))

# This class is used to handle requests to the HTTP server
class RequestHandler(BaseHTTPRequestHandler):
    server = None

    # Used to silence default logging
    def log_message(self, format, *args):
        return

    # Used to send a response to a request
    # response: an instance of RequestResponse
    def send_request_response(self, response):

        # Send HTTP response code and Content-type
        self.send_response(response.status_code)
        self.send_header('Content-type', response.content_type)

        # Send the session key if there is an account
        if response.account is not None:
            self.send_header('Set-Cookie', 'session=' + response.account.session)

        self.end_headers()
        self.wfile.write(response.contents)

    # Used to handle GET and POST requests to the server
    # Serves certain file types, endpoints, or passes the path to ReactJS for a page
    # data: a dict of post data given with the request, if any
    def handle_request(self, data=None):

        path = self.path

        # Create a default response
        # Try to load an account from cookies
        response = RequestResponse(self.load_account_from_cookies())

        try:

            # The request is for an endpoint
            if path.startswith("/api/"):
                path = path[5:]

                # Handle the endpoint request
                # Return if a response was sent
                if self.handle_endpoint_request(path, data, response):
                    return

            else: 
                # The request is for a file or page

                # Check if the request is for one of the allowed file types
                if path.endswith(".js"):
                    response.content_type = "application/javascript"
                elif path.endswith(".css"):
                    response.content_type = "text/css"
                elif path.endswith(".jpg"):
                    response.content_type = "image/jpg"
                elif path.endswith(".gif"):
                    response.content_type = "image/gif"
                elif path.endswith(".png"):
                    response.content_type = "image/png"
                elif path.endswith(".svg"):
                    response.content_type = "image/svg+xml"

                # Redirect to login page if not logged in
                elif path != "/login" and response.account is None:
                    self.send_response(302)
                    self.send_header('Location','/login')
                    self.end_headers()
                    return

                # Redirect from login page to home page if logged in
                elif path == "/login" and response.account is not None:
                    self.send_response(302)
                    self.send_header('Location','/')
                    self.end_headers()
                    return

                else:

                    # Serve the ReactJS index file if the request wasn't handled
                    path = "/index.html"

                # Read file into response contents
                with open("." + path, "rb") as content_file:
                    response.contents = content_file.read()
                    
            # Send response
            self.send_request_response(response)

        except (IOError, KeyError) as e:
            print("exception: " + self.path)
            print(e)
            self.send_error(404,'File Not Found: %s' % self.path)

    # Handles an api request
    # path: The path for the endpoint. E.g path="/ENDPOINT/OPTIONAL_ID"
    # data: The post data sent with the request (if any)
    # response: the current response object. This is modified in this function
    # Returns true if a response was sent
    def handle_endpoint_request(self, path, data, response):

        # Remove trailing "/" if it exists
        index = path.find("/")
        if index == -1:
            endpoint_str = path
        else:
            endpoint_str = path[:index]

        # Try to find the endpoint handler
        try:

            # Create an instance of the endpoint class
            endpoint = RequestHandler.endpoints[endpoint_str]()

        except KeyError:
            print("Tried to connect to non-existent endpoint: {}".format(endpoint_str))

        contents = b""

        # Send "403 forbidden" if endpoint need authorization and request has no valid session
        if (endpoint.needs_auth and response.account is None):

            response.status_code = 403
            contents = b""

        else:

            # If no request data given, try to get an ID from the URL to use for endpoint data
            #       E.g "/api/clientinfo/0"
            if data is None:
                data = -1
                try: 
                    data = path[len(endpoint_str) + 1:]
                    data = int(data)
                except (ValueError, IndexError) as e:
                    pass

            response.content_type = "application/json"

            # Use endpoint to handle request
            contents = endpoint.handle_request(self, self.server.server, response.account, data)

            # Check if the response is a dict
            if hasattr(contents, "keys"):

                # See if the endpoint provided a session and try to use it to get an account
                if "session" in contents.keys():
                    response.account = load_account_from_session(contents["session"])

                # Redirect if the endpoint provided a redirect URL
                if "redirect" in contents.keys():
                    self.send_response(302)
                    self.send_header('Location', contents["redirect"])
                    self.end_headers()
                    return True

            # Turn the endpoint response into JSON
            contents = str.encode(json.dumps(contents))

        response.contents = contents

        # We didn't send a response
        return False

    # Loads an account from request cookies
    def load_account_from_cookies(self):

        # Get any cookies from the request
        cookie_data = self.headers.get('Cookie')

        account = None
        if cookie_data is not None:

            # Parse the cookie data
            parsed_cookie = SimpleCookie(cookie_data)

            cookie = {}

            # Look through cookies for a session
            for c in parsed_cookie.values():

                if c.key == "session":

                    # Check if the session is set and try to load an account from it
                    if c.coded_value != "":
                        account = load_account_from_session(c.coded_value)

                    break

        return account

    # Required method for BaseHTTPRequestHandler
    # Called on GET request
    def do_GET(self):
        self.handle_request()

    # Required method for BaseHTTPRequestHandler
    # Called on HEAD request
    def do_HEAD(self):
        self.send_request_response(RequestResponse())
        
    # Required method for BaseHTTPRequestHandler
    # Called on POST request
    def do_POST(self):

        # Read and parse JSON post data
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode())

        self.handle_request(data)

# This class holds data needed for a typical response
# It's used to pass the data between methods cleanly
class RequestResponse:

    def __init__(self, account=None, status_code=200, content_type="text/html", contents=b""):
        self.account = account
        self.status_code = status_code
        self.content_type = content_type
        self.contents = contents