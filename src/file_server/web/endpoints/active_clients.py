from file_server.web.endpoint import Endpoint

import json

class ActiveClientsEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):
        connections = server.connections

        response = []

        i = 0;
        for conn in connections:
            response.append({
                "id": i,
                "name": conn.account.name,
                "address": conn.address,
                "status": "Idle" if conn.transferring is None else "Transferring Files"
            })
            i += 1

        return response