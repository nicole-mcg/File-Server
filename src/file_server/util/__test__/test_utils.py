import pytest

from file_server.util import split_path

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