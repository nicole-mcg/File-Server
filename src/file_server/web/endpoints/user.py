from file_server.web.endpoint import Endpoint

# This class is used to handle requests for current user information
# This provides a limited amount of information
# This endpoint is for use accross all web pages
class UserEndpoint(Endpoint):
    PATH = "user"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Make sure we've got an account to get information from
        if account is None:

            # Return error to client
            return {"error": "Needs auth"}

        # Return account information
        return {"name": account.name, "refresh_rate": account.settings["refresh_rate"]}