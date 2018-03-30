from .base import Endpoint

import json

from ..account import Account

class LoginEndpoint(Endpoint):

    def handle_request(self, request_handler, server, data):
        name = data["name"]
        password = data["password"]

        account = Account.load_account(name, password)

        if (account is None):
            response = {"error": "Invalid username or password"}
        else:
            response = {"session": account.session}

        return response