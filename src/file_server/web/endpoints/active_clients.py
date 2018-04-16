from file_server.web.endpoint import Endpoint

# This class is used to handle requests for a list of active clients
# This endpoint is used by the home page to poll for current clients
# This endpoint provides limited information on each client. 
# ClientInfoEndpoint is used to provide more in depth client information
class ActiveClientsEndpoint(Endpoint):
    PATH = "activeclients"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Active FileServer connections
        connections = server.connections

        response = []

        # Loop through active connections
        for index, conn in enumerate(connections):

            # Add basic client info to response
            response.append({
                "id": index,
                "name": conn.account.name,
                "address": conn.address,
                "status": "Idle" if conn.transferring is None else "Transferring Files"
            })

        return response