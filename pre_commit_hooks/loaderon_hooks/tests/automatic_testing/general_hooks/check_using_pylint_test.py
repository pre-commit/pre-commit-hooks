import sys
import unittest

import mock
import pytest

from pre_commit_hooks.loaderon_hooks.tests.automatic_testing.util.test_helpers import \
    perform_test_on_file_expecting_result
from pre_commit_hooks.loaderon_hooks.general_hooks.check_using_pylint import main


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []

    # What files should we exclude from pylint checker
    sys.argv.append('--exclude')
    sys.argv.append(r'.*(\/)*incorrect_but_ignored.py')
    yield


def test_with_pylint_ok():
    perform_test_on_file_expecting_result('check_using_pylint_samples/correct.py', main)


def test_with_pylint_ignored():
    perform_test_on_file_expecting_result('check_using_pylint_samples/incorrect_but_ignored.py', main)


def test_with_pylint_error():
    perform_test_on_file_expecting_result('check_using_pylint_samples/incorrect.py', main, expected_result=2)


def walk_return(folder_path):
    root = '/home/administrador/Escritorio/pre-commit-hooks/pre_commit_hooks/loaderon_hooks/tests/automatic_testing/testing_samples/check_using_pylint_samples'
    unused_dirs = []
    files = ['.pylintrc']
    return [(root, unused_dirs, files)]


class TestWithPylintConf(unittest.TestCase):
    @mock.patch('os.walk', side_effect=walk_return)
    def test_with_pylint_conf_ok(self, walk_function):
        perform_test_on_file_expecting_result('check_using_pylint_samples/correct.py', main)
