

# This class represents a web server endpoint
# Calls to endpoints look like this: http://127.0.0.1:8080/api/ENDPOINT/OPTIONAL_ID
# Endpoints take optional POST input (GET can also be used), and return a JSON string to the client
class Endpoint:
    path = ""

    # needs_auth: if true, the endpoint requires a valid session (logged in)
    def __init__(self, needs_auth=True):
        self.needs_auth = needs_auth

    # Handles a request from the HTTP server for the endpoint
    # request_handler: the RequestHandler the HTTP request is associated with
    # server: the FileServer the request is associated with
    # account: the current user account (if any)
    # data: any data for the request:
    #       data is a dict of POST data if it's a POST request
    #       data can be an ID send with a GET request URL (E.g path="/ENDPOINT/OPTIONAL_ID")
    def handle_request(self, request_handler, server, account, data):
        return None