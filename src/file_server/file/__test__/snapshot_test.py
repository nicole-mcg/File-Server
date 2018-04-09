# content of test_sample.py

import pytest

from file_server.file.snapshot import Snapshot, FileSnapshot, DirectorySnapshot

import inspect, os, json

@pytest.mark.parametrize("path,parts", [
    ("C:/test1", ["C:/", "test1"]),
    ("/usr/", ["/", "usr"]),
    ("./img/test1/test2", [".", "img", "test1", "test2"]),
    ("../img", ["..", "img"]),
    ("hello/img/", ["hello", "img"]),
])
def test_split(path, parts):
    split = DirectorySnapshot.split_path(path);

    assert len(split) == len(parts)

    for index, part in enumerate(parts):
        assert split[index] == part

def test_directory_snapshot():
    curr_path = os.path.split(inspect.stack()[0][1])[0]
    path = curr_path + "/bin/test_dir"

    def confirm_snapshot(expected_snapshots, snapshot, root_path, path=""):

        if hasattr(snapshot, "snapshots"):
             #Make sure the number of files (and folders) are what we expected
            assert len(expected_snapshots) == len(snapshot.snapshots)

        #Loop through expected files
        for key in expected_snapshots.keys():

            #Make sure the file is in the snapshot
            assert key in snapshot.snapshots

            tmp_snap = snapshot.snapshots[key]
            tmp_path = "{}{}".format(path, tmp_snap.file_name)

            #Double check the file name
            assert tmp_snap.file_name == key

            #Make sure the snapshot's paths are what we expected
            assert tmp_snap.rel_path == tmp_path
            assert tmp_snap.full_path == "{}/{}".format(root_path, tmp_path)

            #Confirm that snapshot too
            confirm_snapshot(expected_snapshots[key], tmp_snap, root_path, tmp_path + "/")

    def confirm_json(expected_snapshots, snapshot_dict):

        if "snapshots" in snapshot_dict:
            assert snapshot_dict["type"] == 1

            #Loop through expected files
            for key in expected_snapshots.keys():

                snapshots = snapshot_dict["snapshots"]

                #Make sure we have the right amount of files
                assert len(expected_snapshots) == len(snapshots)

                #Make sure all the files we expected are there
                found = -1
                for index, snapshot in enumerate(snapshots):
                    if snapshot["file_name"] == key:
                        found = index
                assert found != -1

                confirm_json(expected_snapshots[key], snapshots[found])

        else:
            assert snapshot_dict["type"] == 2

        

    snapshots = {
        "test2": {
            "img2.bmp": {},
            "txt2.txt": {}
        },
        "test3": {
            "test4": {
                "img4.bmp": {},
                "txt4.txt": {}
            }
        },
        "img1.bmp": {},
        "txt1.txt": {}
    }
    
    test_snapshot = DirectorySnapshot(path, "test_dir", path)
    confirm_snapshot(snapshots, test_snapshot, path)
    confirm_json(snapshots, json.loads(test_snapshot.to_json()))