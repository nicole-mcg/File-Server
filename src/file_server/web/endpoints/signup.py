from .base import Endpoint

import json, os

from ..account import Account

class SignupEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = False

    def handle_request(self, request_handler, server, account, data):
        name = data["name"]
        password = data["password"]

        if "auth_code" in data:
            account = Account.create_account(name, password, data["auth_code"])
            if (account is None):
                return {"error": "Account already exists"}
            else:
                return {"session": account.session}

        if not os.path.isdir("../bin/accounts/") or len(os.listdir("../bin/accounts/")) == 0:
            account = Account.create_account(name, password, Account.create_auth())
            return {"session": account.session}

        return {"needs_auth": True}