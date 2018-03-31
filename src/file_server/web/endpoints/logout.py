from .base import Endpoint

import json

from ..account import Account

class LogoutEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        Account.end_session(account.session)

        return {"redirect": "/login"}