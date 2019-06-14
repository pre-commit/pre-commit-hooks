import sys

import pytest

from pre_commit_hooks.loaderon_hooks.general_hooks.check_xml_encoding import main
from pre_commit_hooks.loaderon_hooks.tests.util.test_helpers import perform_test_on_file_expecting_result


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []

    # Encoding to be checked
    sys.argv.append('--encoding')
    sys.argv.append(r'<?xml version="1.0" encoding="utf-8"?>')
    yield


def test_check_xml_encoding_ok():
    perform_test_on_file_expecting_result('check_xml_encoding_samples/ok.xml', main)


def test_check_xml_encoding_error_1():
    perform_test_on_file_expecting_result('check_xml_encoding_samples/no_encoding.xml', main, expected_result=2)


def test_check_xml_encoding_error_2():
    perform_test_on_file_expecting_result('check_xml_encoding_samples/first_line_is_empty_space.xml',
                                          main,
                                          expected_result=2)
