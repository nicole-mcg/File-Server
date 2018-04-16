from file_server.web.endpoint import Endpoint

import json

class DirectoryContentsEndpoint(Endpoint):
    PATH = "directorycontents"

    def __init__(self):
        Endpoint.__init__(self)

    def handle_request(self, request_handler, server, account, data):

        response = {"error": "Could not load path"}
        try:
            response = json.loads(server.directory_snapshot.to_json(data["path"], False))
        except KeyError as e:
            print("KeyError: " + str(e))

        return response