from file_server.web.endpoint import Endpoint

import json

from file_server.account.account_manager import update_settings

class UpdateSettingsEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        update_settings(account, data)

        return {}