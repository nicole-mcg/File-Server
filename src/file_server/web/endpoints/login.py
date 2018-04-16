from file_server.web.endpoint import Endpoint

from file_server.account.account_manager import load_account

# This class is used to handle requests for logging in
class LoginEndpoint(Endpoint):
    PATH = "login"

    # Need to override parent __init__ to specify we don't need a valid session
    def __init__(self):
        Endpoint.__init__(self, False)

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Make sure the username and password was provided
        if not "name" in data and not "password" in data:
            return {"error": "You must provide a username and password"}

        # Try to load an account with provided credentials
        account = load_account(data["name"], data["password"])

        # Couldn't load account
        # This could be because the account doesn't exist, or the password is incorrect
        if (account is None):
            return {"error": "Invalid username or password"}
        
        # Return the newly created session
        # the "session" key will trigger the webserver to add a session cookie with the response
        return {
            "session": account.session,
            "auth_code": account.auth_code,
            "settings": account.settings
        }