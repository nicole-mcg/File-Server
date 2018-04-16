from file_server.web.endpoint import Endpoint

import json

from file_server.account.account_manager import create_signup_auth

class CreateAuthEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):
        return {"new_auth": create_signup_auth()}