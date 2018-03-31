from .base import Endpoint

import json

from ..account import Account

class LoginEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = False

    def handle_request(self, request_handler, server, account, data):
        name = data["name"]
        password = data["password"]

        account = Account.load_account(name, password)

        if (account is None):
            response = {"error": "Invalid username or password"}
        else:
            response = {
                "session": account.session,
                "auth_code": account.auth_code,
                "settings": account.settings,
            }

        return response