# This file is run in the pytest environment before the tests

import pytest
import webbrowser

# This method is called before all tests
# It's used to override any methods
@pytest.fixture()
def prepare_for_tests():

    def empty_function(url, **kwargs):
        pass

    # Override webbrowser.open so test can't open pages on the internet
    webbrowser.open = empty_function