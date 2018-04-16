import pytest
import tempfile
import webbrowser

@pytest.fixture()
def prepare_for_tests():

    def empty_function(url, **kwargs):
        pass

    webbrowser.open = empty_function