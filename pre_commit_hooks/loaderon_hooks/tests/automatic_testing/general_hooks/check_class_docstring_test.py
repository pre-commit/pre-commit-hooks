import os
import sys

import pytest

from pre_commit_hooks.loaderon_hooks.general_hooks.check_class_docstring import main


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []
    yield


def get_sample_file_path(file_name):
    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testing_files_folder_path = current_path + '/testing_files/class_docstring_samples/'
    return testing_files_folder_path + file_name


def perform_test_on_file_expecting_result(file_name, expected_result=0):
    sample_file_path = get_sample_file_path(file_name)
    sys.argv.append(sample_file_path)

    result = main(sys.argv)

    assert result == expected_result


def test_docstring_ok():
    perform_test_on_file_expecting_result('docstring_ok.py')


def test_docstring_error_1():
    perform_test_on_file_expecting_result('docstring_error_1.py', expected_result=2)


def test_docstring_error_2():
    perform_test_on_file_expecting_result('docstring_error_2.py', expected_result=2)


def test_docstring_error_3():
    perform_test_on_file_expecting_result('docstring_error_3.py', expected_result=2)


def test_docstring_error_4():
    perform_test_on_file_expecting_result('docstring_error_4.py', expected_result=2)


def test_docstring_error_5():
    perform_test_on_file_expecting_result('docstring_error_5.py', expected_result=2)


def test_docstring_error_6():
    perform_test_on_file_expecting_result('docstring_error_6.py', expected_result=2)


def test_docstring_error_7():
    perform_test_on_file_expecting_result('docstring_error_7.py', expected_result=2)
