from .base import Endpoint

import json

class UserEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        if account is None:
            return {"needs_auth": True}

        return {"name": account.name}