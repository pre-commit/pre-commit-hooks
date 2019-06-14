import sys

import pytest

from pre_commit_hooks.loaderon_hooks.tests.util.test_helpers import perform_test_on_file_expecting_result
from pre_commit_hooks.loaderon_hooks.general_hooks.check_location import main


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []

    # Each line is a directory that allows certain types of files.
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/xml')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/javascript')

    # Each line specifies what types of files can be located inside the directory.
    sys.argv.append('--files')
    sys.argv.append(r'correct_xml.xml')
    sys.argv.append('--files')
    sys.argv.append(r'correct_js.js')
    yield


def test_locations_ok_1():
    perform_test_on_file_expecting_result('check_location_samples/xml/correct_xml.xml', main)


def test_locations_ok_2():
    perform_test_on_file_expecting_result('check_location_samples/javascript/correct_js.js', main)


def test_locations_error1():
    perform_test_on_file_expecting_result('check_location_samples/xml/incorrect_js.js', main, expected_result=2)


def test_locations_error2():
    perform_test_on_file_expecting_result('check_location_samples/not_enabled_directory/incorrect_xml.xml', main, expected_result=2)


def test_locations_arguments_size_mismatch_error():
    sys.argv = []

    sys.argv.append('--directories')
    sys.argv.append(r'.*\/xml')
    # Lacking files for this directory
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/javascript')

    sys.argv.append('--files')
    sys.argv.append(r'correct_xml.xml')

    perform_test_on_file_expecting_result('check_location_samples/xml/correct_xml.xml', main, expected_result=2)


def test_locations_no_arguments_error():
    sys.argv = []
    with pytest.raises(TypeError) as error:
        perform_test_on_file_expecting_result('check_location_samples/xml/correct_xml.xml', main)
    assert "'NoneType' object is not iterable" in str(error.value)
