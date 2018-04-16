from file_server.web.endpoint import Endpoint

import json, os

from file_server.account.account_manager import is_valid_signup_auth, create_account

class SignupEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = False

    def handle_request(self, request_handler, server, account, data):
        print("signup endpoint")
        if data["name"] == "" or data["password"] == "":
            return {"error": "Invalid username or password"}

        name = data["name"]
        password = data["password"]

        auth = ""
        if "auth_code" in data:
            auth = data["auth_code"]

        if is_valid_signup_auth(auth):
            account = create_account(name, password, auth)
            if (account is None):
                return {"error": "Account already exists"}
            else:
                return {"session": account.session}

        return {"error": "needs auth"}