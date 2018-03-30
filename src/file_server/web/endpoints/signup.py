from .base import Endpoint

import json, os

from ..account import Account

class SignupEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = False

    def handle_request(self, request_handler, server, account, data):
        name = data["name"]
        password = data["password"]

        if not os.path.isdir("../bin/accounts/") or len(os.listdir("../bin/accounts/")) == 0:
            account = Account.create_account(name, password, Account.create_auth())
            if (account is None):
                response = {"error": "Invalid username or password"}
            else:
                response = {"session": account.session}
        else:
            response = {"needs_auth": True}
        return response