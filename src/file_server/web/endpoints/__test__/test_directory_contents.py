
import pytest

from file_server.web.endpoints.directory_contents import DirectoryContentsEndpoint

from file_server.util import create_object

from file_server.util.test_util import start_test_server

def test_directory_contents():

    def to_json(path, recursive):
        snapshot_json = '{"type": 2, "file_name": "0", "full_path": "0", "last_modified": 0}'
        if path == "./":
            return '{"type": 1, file_name"="/" "full_path": ".", "last_modified": 0, "snapshots": [{}]'.format(snapshot_json)
        if path == "./0": 
            return snapshot_json

    data = {
        "path": "./"
    }

    server = create_object({
        "hub_processor": create_object({
            "snapshot": create_object({
                "to_json": to_json
            })
        })
    })

    thread = start_test_server()

    import pdb; pdb.set_trace();

    print(thread)

    DirectoryContentsEndpoint().handle_request(None, server, None, data)

    assert False