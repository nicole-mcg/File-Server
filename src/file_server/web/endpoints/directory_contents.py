from .base import Endpoint

import json

class DirectoryContentsEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):
        return json.loads(server.hub_processor.snapshot.to_json(data["path"], False))