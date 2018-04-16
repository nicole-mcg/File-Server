import json

from file_server.web.endpoint import Endpoint

# This class is used to handle requests for contents of a single directory on the file watch path (non-recursive)
# This class is used by the Files web page to load contents for each directory as it's opened
class DirectoryContentsEndpoint(Endpoint):
    PATH = "directorycontents"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Try to get the path from the current directory snapshot
        try:
            return json.loads(server.directory_snapshot.to_json(data["path"], False))
        except KeyError as e:

            # Presumably, the path doesn't exist
            print(e)
            return {"error": "Could not load path"}