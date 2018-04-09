import pytest

from file_server.util import split_path, create_object

@pytest.mark.parametrize("path,parts", [
    ("C:/test1", ["C:/", "test1"]),
    ("/usr/", ["/", "usr"]),
    ("./img/test1/test2", [".", "img", "test1", "test2"]),
    ("../img", ["..", "img"]),
    ("hello/img/", ["hello", "img"]),
])
def test_split(path, parts):
    split = split_path(path);

    assert len(split) == len(parts)

    for index, part in enumerate(parts):
        assert split[index] == part

@pytest.mark.parametrize("obj_dict", [
    ({
        "test": "test2",
        "dict": {
            "nested": "works",
            "again": {
                "working": "yes"
            }
        }
    }),
])
def test_create_object(obj_dict):

    test_obj = create_object(obj_dict)

    for key in obj_dict.keys():

        #Verify all dict entries were turned into attributes
        assert hasattr(test_obj, key)

        #Test this one too
        if (hasattr(obj_dict[key], "keys")):
            test_create_object(obj_dict[key])