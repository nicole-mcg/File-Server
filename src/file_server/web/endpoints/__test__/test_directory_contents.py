# Author: Connor McGrogan

# Import test utilities
from file_server.util._test_util import start_test_server, send_test_api_request

# json.loads is used to turn a JSON string into a Python dict
import json

# Tests the directory contents endpoint
def test_directory_contents():

    # Create a test server
    server = start_test_server()

    # Signup so we have authentication for directorycontents
    response = send_test_api_request("signup", {"name": "test", "password": "test"})
    assert response is not None

    #Load the session key
    response = json.loads(response)
    assert "session" in response # Making the test fail by assertion rather than KeyError makes it more clear that something is wrong
    session = response["session"]

    # Get directory contents from server
    response = send_test_api_request("directorycontents", {"path": "./"}, session)
    assert response is not None

    # Verify the server respose is the same as the json generated directly from the server
    assert response == str(server.file_processor.snapshot)

    # Send request with invalid path
    response = send_test_api_request("directorycontents", {"path": "./hello"}, session)
    assert response is not None

    # Verify the server gave as an error
    response = json.loads(response)
    assert "error" in response

    # Verify the error is what we expected
    assert response["error"] == "Could not load path"

    # Shutdown the test server
    server.kill()