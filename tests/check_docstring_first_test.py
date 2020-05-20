import pytest

from pre_commit_hooks.check_docstring_first import check_docstring_first
from pre_commit_hooks.check_docstring_first import main


# Contents, expected, expected_output
TESTS = (
    # trivial
    (b'', 0, ''),
    # Acceptable
    (b'"foo"', 0, ''),
    # Docstring after code
    (
        b'from __future__ import unicode_literals\n'
        b'"foo"\n',
        1,
        '{filename}:2 Module docstring appears after code '
        '(code seen on line 1).\n',
    ),
    # Test double docstring
    (
        b'"The real docstring"\n'
        b'from __future__ import absolute_import\n'
        b'"fake docstring"\n',
        1,
        '{filename}:3 Multiple module docstrings '
        '(first docstring on line 1).\n',
    ),
    # Test multiple lines of code above
    (
        b'import os\n'
        b'import sys\n'
        b'"docstring"\n',
        1,
        '{filename}:3 Module docstring appears after code '
        '(code seen on line 1).\n',
    ),
    # String literals in expressions are ok.
    (b'x = "foo"\n', 0, ''),
)


all_tests = pytest.mark.parametrize(
    ('contents', 'expected', 'expected_out'), TESTS,
)


@all_tests
def test_unit(capsys, contents, expected, expected_out):
    assert check_docstring_first(contents) == expected
    assert capsys.readouterr()[0] == expected_out.format(filename='<unknown>')


@all_tests
def test_integration(tmpdir, capsys, contents, expected, expected_out):
    f = tmpdir.join('test.py')
    f.write_binary(contents)
    assert main([str(f)]) == expected
    assert capsys.readouterr()[0] == expected_out.format(filename=str(f))


def test_arbitrary_encoding(tmpdir):
    f = tmpdir.join('f.py')
    contents = '# -*- coding: cp1252\nx = "£"'.encode('cp1252')
    f.write_binary(contents)
    assert main([str(f)]) == 0
