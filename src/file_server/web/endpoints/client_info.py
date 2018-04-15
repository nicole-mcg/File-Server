from .base import Endpoint

import json

class ClientInfoEndpoint(Endpoint):

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):
        connections = server.connections

        try:
            conn = connections[data]

            return {
                "name": conn.account.name,
                "address": conn.address,
                "status": "Idle" if conn.transferring is None else "Transferring Files",
                "time": conn.connect_time,
                "files_sent": conn.files_sent,
                "data_sent": conn.data_sent,
                "files_recieved": conn.files_recieved,
                "data_recieved": conn.data_recieved,
                "transferring": conn.transferring,
                "transfer_progress": conn.transfer_progress,
                "queued_packets": len(conn.packet_queue) + len(server.buffer_queue),
                "events_to_ignore": len(conn.file_event_handler.events_to_ignore),
            }

        except KeyError:
            pass

        return {}