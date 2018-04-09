from .base import Endpoint

import json

from ..account import Account

class UpdateSettingsEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        account.update_settings(data)

        return {}