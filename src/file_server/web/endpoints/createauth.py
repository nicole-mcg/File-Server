from .base import Endpoint

import json

from ..account import Account

class CreateAuthEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):
        return {"new_auth": Account.create_auth()}