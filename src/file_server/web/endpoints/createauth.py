from file_server.web.endpoint import Endpoint

from file_server.account.account_manager import create_signup_auth

# This class is used to handle requests for a newly generated auth code for signup
class CreateAuthEndpoint(Endpoint):
    PATH = "createauth"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):
        return {"new_auth": create_signup_auth()}