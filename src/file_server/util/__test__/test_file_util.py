import pytest

from file_server.util import split_path

# Paramaterize will call this test multiple times with different parameters
@pytest.mark.parametrize("path,parts", [
    ("C:/test1", ["C:/", "test1"]),
    ("/usr/", ["/", "usr"]),
    ("./img/test1/test2", [".", "img", "test1", "test2"]),
    ("../img", ["..", "img"]),
    ("hello/img/", ["hello", "img"]),
])
# path: the path to split
# parts: a list of the expected parts
def test_split(path, parts):
    split = split_path(path)

    # Make sure we have the right number of parts
    assert len(split) == len(parts)

    # Make sure each part is the same
    for index, part in enumerate(parts):
        assert split[index] == part