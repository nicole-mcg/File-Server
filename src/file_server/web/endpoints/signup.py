from .base import Endpoint

import json, os

from ..account import Account

class SignupEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = False

    def handle_request(self, request_handler, server, account, data):
        if data["name"] == "" or data["password"] == "":
            return {"error": "Invalid username or password"}

        name = data["name"]
        password = data["password"]

        if "auth_code" in data or Account.is_valid_auth(""):
            account = Account.create_account(name, password, data["auth_code"])
            if (account is None):
                return {"error": "Account already exists"}
            else:
                return {"session": account.session}

        return {"needs_auth": True}