import sys

import pytest

from pre_commit_hooks.loaderon_hooks.tests.automatic_testing.util.test_helpers import \
    perform_test_on_file_expecting_result
from pre_commit_hooks.loaderon_hooks.general_hooks.check_line import main


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []

    # Multiple checks, one regexp per type of line to check.
    sys.argv.append('--line-to-check')
    sys.argv.append(r'^(\t| )*<field.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'^(\t| )*<record.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'.+fields.Many2one.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'.+fields.One2many.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'.+fields.Many2many.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'class.+')

    # Regexp for knowing how the line must be in order to be correct.
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*<field name=".+"')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*<record id=".+"')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*.+_id = fields.Many2one\(')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*.+_ids = fields.One2many\(')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*.+_ids = fields.Many2many\(')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'class ([A-Z]+[a-z0-9]+)+\(models.Model\):')
    yield


def test_odoo_xml_field_and_record_declaration_ok():
    perform_test_on_file_expecting_result('check_line_samples/xml_lines_ok.xml', main)


def test_odoo_xml_record_declaration_error():
    perform_test_on_file_expecting_result('check_line_samples/xml_lines_error_1.xml', main, expected_result=2)
