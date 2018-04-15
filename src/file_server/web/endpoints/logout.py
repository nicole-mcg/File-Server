from .base import Endpoint

import json

from file_server.account.account_manager import end_session

class LogoutEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        end_session(account.session)

        return {"redirect": "/login"}