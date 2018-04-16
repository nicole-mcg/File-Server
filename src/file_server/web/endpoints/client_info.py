from file_server.web.endpoint import Endpoint

# This class is used to handle requests for in-depth information on a single client
# The endpoint is used by the ClientInfo web widget to show client transfer information
class ClientInfoEndpoint(Endpoint):
    PATH = "clientinfo"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Try to get the active client by index
        try:
            conn = server.connections[data]
        except KeyError:
            return {"error": "Client index doesn't exist"}

        # Return client information
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