from __future__ import annotations

import pytest

from pre_commit_hooks.check_fluent import main


def test_valid_fluent_file(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text(
        'hello = Hello, world!\n'
        'greeting = Hello, { $name }!\n'
        '    .title = Greeting\n'
        'menu-item = Menu Item\n',
    )
    assert main([str(f)]) == 0


def test_fluent_file_with_select_expression(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text(
        'emails = { $unreadEmails ->\n'
        '    [0] You have no unread emails.\n'
        '    [one] You have one unread email.\n'
        '   *[other] You have { $unreadEmails } unread emails.\n'
        '}\n',
    )
    assert main([str(f)]) == 0


def test_fluent_file_with_comments(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text(
        '# This is a comment\n'
        'hello = Hello, world!\n'
        '\n'
        '## Another comment\n'
        'goodbye = Goodbye!\n',
    )
    assert main([str(f)]) == 0


def test_fluent_file_with_invalid_identifier(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text('123invalid = Invalid identifier\n')
    assert main([str(f)]) == 1


def test_fluent_file_with_invalid_attribute_identifier(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text('hello = Hello\n' '    .123invalid = Invalid attribute\n')
    assert main([str(f)]) == 1


def test_fluent_file_missing_default_variant(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text(
        'emails = { $unreadEmails ->\n'
        '    [0] You have no unread emails.\n'
        '    [one] You have one unread email.\n'
        '}\n',
    )
    assert main([str(f)]) == 1


def test_fluent_file_variant_outside_select(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text('hello = Hello\n' '   *[default] This should not be here\n')
    assert main([str(f)]) == 1


def test_fluent_file_missing_indentation(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text('hello = Hello\n' '.title = This should be indented\n')
    assert main([str(f)]) == 1


def test_fluent_file_indented_without_context(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text('    orphaned = This line has no message context\n')
    assert main([str(f)]) == 1


def test_non_utf8_file(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_bytes(b'\xa9\xfe\x12')
    assert main([str(f)]) == 1


def test_nonexistent_file():
    assert main(['nonexistent.ftl']) == 1


def test_empty_file(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text('')
    assert main([str(f)]) == 0


def test_multiple_files(tmp_path):
    f1 = tmp_path / 'valid.ftl'
    f1.write_text('hello = Hello, world!\n')

    f2 = tmp_path / 'invalid.ftl'
    f2.write_text('123invalid = Invalid identifier\n')

    assert main([str(f1), str(f2)]) == 1


def test_multiple_valid_files(tmp_path):
    f1 = tmp_path / 'valid1.ftl'
    f1.write_text('hello = Hello, world!\n')

    f2 = tmp_path / 'valid2.ftl'
    f2.write_text('goodbye = Goodbye!\n')

    assert main([str(f1), str(f2)]) == 0


@pytest.mark.parametrize(
    'identifier,expected',
    [
        ('hello', True),
        ('hello-world', True),
        ('hello_world', True),
        ('hello123', True),
        ('123hello', False),
        ('hello-', True),
        ('-hello', False),
        ('', False),
        ('hello.world', False),
        ('hello world', False),
    ],
)
def test_identifier_validation(identifier, expected):
    from pre_commit_hooks.check_fluent import _is_valid_identifier

    assert _is_valid_identifier(identifier) == expected


def test_fluent_file_non_default_variant_with_closing_brace(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text(
        'emails = { $unreadEmails ->\n'
        '    [0] You have no unread emails. }\n',
    )
    assert main([str(f)]) == 1  # Should fail due to missing default variant


def test_fluent_file_non_star_variant_with_closing_check(tmp_path):
    f = tmp_path / 'test.ftl'
    f.write_text(
        'test = { $var ->\n'
        '    [case]\n'        # Comment
        '        Value here\n'
        '   *[other] Default\n'
        '}\n',
    )
    assert main([str(f)]) == 0
