
import pytest

from file_server.web.endpoints.active_clients import ActiveClientsEndpoint

from file_server.util import create_object

def test_active_clients():

    def createConnectionObj(client_host, account_name, transferring=False):
        return create_object({
            "client_host": client_host,
            "account": create_object({"name": account_name}),
            "transferring": transferring,
        })

    connections = [
        createConnectionObj("client host", "account name", True)
    ]

    ActiveClientsEndpoint().handle_request(None, create_object({"connections": connections}), None, None)
    
    assert True