from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.check_docstring_first import check_docstring_first
from pre_commit_hooks.check_docstring_first import main


# Contents, expected, expected_output
TESTS = (
    # trivial
    ('', 0, ''),
    # Acceptable
    ('"foo"', 0, ''),
    # Docstring after code
    (
        'from __future__ import unicode_literals\n'
        '"foo"\n',
        1,
        '{filename}:2 Module docstring appears after code '
        '(code seen on line 1).\n',
    ),
    # Test double docstring
    (
        '"The real docstring"\n'
        'from __future__ import absolute_import\n'
        '"fake docstring"\n',
        1,
        '{filename}:3 Multiple module docstrings '
        '(first docstring on line 1).\n',
    ),
    # Test multiple lines of code above
    (
        'import os\n'
        'import sys\n'
        '"docstring"\n',
        1,
        '{filename}:3 Module docstring appears after code '
        '(code seen on line 1).\n',
    ),
    # String literals in expressions are ok.
    ('x = "foo"\n', 0, ''),
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
    f.write(contents)
    assert main([f.strpath]) == expected
    assert capsys.readouterr()[0] == expected_out.format(filename=f.strpath)
