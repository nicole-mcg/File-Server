from .base import Endpoint

import json

class ActiveClientsEndpoint(Endpoint):

    def handle_request(self, request_handler, server, id):
        connections = server.connections

        response = []

        i = 0;
        for conn in connections:
            response.append({
                "id": i,
                "address": conn.client_host,
                "status": "Idle" if conn.transferring is None else "Transferring Files"
            })
            i += 1

        return json.dumps(response)