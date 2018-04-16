from file_server.web.endpoint import Endpoint

from file_server.account.account_manager import is_valid_signup_auth, create_account

# This class is used to handle requests for signing up
class SignupEndpoint(Endpoint):
    PATH = "signup"

    # Need to override parent __init__ to specify we don't need a valid session
    def __init__(self):
        Endpoint.__init__(self, False)

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Make sure the username and password was provided
        if data["name"] == "" or data["password"] == "":
            return {"error": "You must provide a username and password"}

        # Try to get an auth code from the request
        auth = ""
        if "auth_code" in data:
            auth = data["auth_code"]

        # Make sure auth code is valid
        if not is_valid_signup_auth(auth):
            return {"error": "Needs auth"}

        # Try to create an account with the specified credentials
        account = create_account(data["name"], data["password"], auth)

        # Make sure account was created successfully
        # Account creation can fail because the account exists or the auth is invalid (we've already checked the auth)
        if (account is None):
            return {"error": "Account already exists"}
        
        # Return the newly created account session
        # The "session" key will trigger the webserver to send a session cookie with the response
        return {"session": account.session}