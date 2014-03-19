
import __builtin__

import mock
import pytest


@pytest.yield_fixture
def print_mock():
    with mock.patch.object(__builtin__, 'print', autospec=True) as mock_print:
        yield mock_print
