from .base import Endpoint

import json

class DirectoryContentsEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        response = {"error": "Could not load path"}
        try:
            response = json.loads(server.hub_processor.snapshot.to_json(data["path"], False))
        except KeyError as e:
            print("KeyError: " + str(e))

        return response