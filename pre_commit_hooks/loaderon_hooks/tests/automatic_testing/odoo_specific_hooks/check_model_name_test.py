import sys

import pytest

from pre_commit_hooks.loaderon_hooks.odoo_specific_hooks.check_model_name import main
from pre_commit_hooks.loaderon_hooks.tests.automatic_testing.util.test_helpers import \
    perform_test_on_file_expecting_result


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []
    yield


def test_check_model_name_ok():
    perform_test_on_file_expecting_result('check_model_name_samples/ok.py', main)


def test_check_model_name_multiple_inheritance_ok():
    perform_test_on_file_expecting_result('check_model_name_samples/multiple_inheritance_ok.py', main)


def test_check_model_name_error():
    perform_test_on_file_expecting_result('check_model_name_samples/error.py', main, expected_result=2)
