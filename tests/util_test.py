
import mock
import pytest
import sys

from pre_commit_hooks.util import entry


@pytest.fixture
def entry_func():
    @entry
    def func(argv):
        return argv

    return func


def test_explicitly_passed_argv_are_passed(entry_func):
    input = object()
    ret = entry_func(input)
    assert ret is input


def test_no_arguments_passed_uses_argv(entry_func):
    argv = [1, 2, 3, 4]
    with mock.patch.object(sys, 'argv', argv):
        ret = entry_func()
        assert ret == argv[1:]
