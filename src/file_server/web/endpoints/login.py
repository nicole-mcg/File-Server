from file_server.web.endpoint import Endpoint

import json

from file_server.account.account_manager import load_account

class LoginEndpoint(Endpoint):

    def __init__(self):
        Endpoint.__init__(self, False)

    def handle_request(self, request_handler, server, account, data):
        name = data["name"]
        password = data["password"]

        account = load_account(name, password)

        if (account is None):
            response = {"error": "Invalid username or password"}
        else:
            response = {
                "session": account.session,
                "auth_code": account.auth_code,
                "settings": account.settings,
            }

        return response