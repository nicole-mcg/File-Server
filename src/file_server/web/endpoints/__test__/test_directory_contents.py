
import pytest

from file_server.web.endpoints.directory_contents import DirectoryContentsEndpoint
from file_server.util import create_object, send_api_request
from file_server.util.test_util import start_test_server
from file_server.web.account import Account

import os, inspect, json

def test_directory_contents():

    curr_path = os.path.split(inspect.stack()[0][1])[0]

    server = start_test_server(curr_path)

    print(1)

    # Signup so we have authentication for directorycontents
    response = send_api_request("signup", "", {"name": "test", "password": "test"}, 8081)
    assert response is not None
    response = json.loads(response)
    assert "session" in response

    print(2)

    # Get directory contents
    response = send_api_request("directorycontents", response["session"], {"path": "./"}, 8081)
    assert response is not None

    assert response == str(server.hub_processor.snapshot)