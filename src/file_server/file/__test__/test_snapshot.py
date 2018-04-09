# content of test_sample.py

import pytest

from file_server.file.snapshot import Snapshot, FileSnapshot, DirectorySnapshot

import inspect, os, json

def test_snapshot():
    curr_path = os.path.split(inspect.stack()[0][1])[0]
    path = curr_path + "/test_dir"

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

        if not "snapshots" in snapshot_dict:
            #It's not a directory
            assert snapshot_dict["type"] == 2
            return

        assert snapshot_dict["type"] == 1

        #Loop through expected files
        for key in expected_snapshots.keys():

            snapshots = snapshot_dict["snapshots"]

            #Make sure we have the right amount of files
            assert len(expected_snapshots) == len(snapshots)

            #Make sure all the files we expected are there
            index = -1
            for i, snapshot in enumerate(snapshots):
                if snapshot["file_name"] == key:
                    index = i
            assert index != -1

            confirm_json(expected_snapshots[key], snapshots[index])

    #The expected snapshot dict to test against
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
    
    #Create the snapshot
    test_snapshot = DirectorySnapshot(path, "test_dir", path)

    #Confirm Snapshot class structure is correct
    confirm_snapshot(snapshots, test_snapshot, path)

    #Confirm snapshot to json is correct
    confirm_json(snapshots, json.loads(test_snapshot.to_json()))
