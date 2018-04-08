from .base import Endpoint

import json

class DirectoryContentsEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):

        data = {"error": "Could not find path"}
        try:
            data = json.loads(server.hub_processor.snapshot.to_json(data["path"], False))
        except Error as e:
            print("Error trying to get directory contents: path=" + data["path"])
            print(e)

        return data