from .base import Endpoint

import json

class ActiveClientsEndpoint(Endpoint):

    def handle_request(self, request_handler, server):
        connections = server.connections

        response = []

        for conn in connections:
            response.append({
                "address": conn.client_host,
                "time": conn.connect_time,
                "files_sent": conn.files_sent,
                "data_sent": conn.data_sent,
                "files_recieved": conn.files_recieved,
                "data_recieved": conn.data_recieved,
                "transferring": conn.transferring,
                "transfer_progress": conn.transfer_progress,
                "queued_packets": len(conn.packet_queue)
            })

        return json.dumps(response)