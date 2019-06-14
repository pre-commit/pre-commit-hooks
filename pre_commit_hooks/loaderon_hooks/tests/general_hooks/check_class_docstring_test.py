import sys

import pytest

from pre_commit_hooks.loaderon_hooks.tests.util.test_helpers import perform_test_on_file_expecting_result
from pre_commit_hooks.loaderon_hooks.general_hooks.check_class_docstring import main


@pytest.fixture(autouse=True)
def clean_():
    sys.argv = []
    yield


def test_docstring_ok():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_ok.py', main)


def test_docstring_error_1():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_1.py', main, expected_result=2)


def test_docstring_error_2():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_2.py', main, expected_result=2)


def test_docstring_error_3():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_3.py', main, expected_result=2)


def test_docstring_error_4():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_4.py', main, expected_result=2)


def test_docstring_error_5():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_5.py', main, expected_result=2)


def test_docstring_error_6():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_6.py', main, expected_result=2)


def test_docstring_error_7():
    perform_test_on_file_expecting_result('check_class_docstring_samples/docstring_error_7.py', main, expected_result=2)
