from file_server.web.endpoint import Endpoint

from file_server.account.account_manager import end_session

# This class is used to handle requests for logging out
class LogoutEndpoint(Endpoint):
    PATH = "logout"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # End the current account session
        end_session(account.session)

        # The "redirect" key will trigger the webserver to redirect to another page
        return {"redirect": "/login"}