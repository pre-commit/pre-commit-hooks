import sys

import pytest

from pre_commit_hooks.loaderon_hooks.odoo_specific_hooks.check_view_fields_order import main
from pre_commit_hooks.loaderon_hooks.tests.automatic_testing.util.test_helpers import \
    perform_test_on_file_expecting_result


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []
    yield


def test_check_view_fields_order_ok():
    perform_test_on_file_expecting_result('check_view_fields_order_samples/ok.xml', main)


def test_check_view_fields_order_multiple_records_ok():
    perform_test_on_file_expecting_result('check_view_fields_order_samples/multiple_records_ok.xml', main)


def test_check_view_fields_order_name_error():
    perform_test_on_file_expecting_result('check_view_fields_order_samples/first_field_not_name_error.xml', main, expected_result=2)


def test_check_view_fields_order_model_error():
    perform_test_on_file_expecting_result('check_view_fields_order_samples/second_field_not_model_error.xml', main, expected_result=2)
