from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.string_fixer import main

TESTS = (
    # Base cases
    (
        "''",
        "''",
        0
    ),
    (
        '""',
        "''",
        1
    ),
    (
        r'"\'"',
        r'"\'"',
        0
    ),
    (
        r'"\""',
        r'"\""',
        0
    ),
    (
        r"'\"\"'",
        r"'\"\"'",
        0
    ),
    # String somewhere in the line
    (
        'x = "foo"',
        "x = 'foo'",
        1
    ),
    # Test escaped characters
    (
        r'"\'"',
        r'"\'"',
        0
    ),
    # Docstring
    (
        '""" Foo """',
        '""" Foo """',
        0
    ),
    # Fuck it, won't even try to fix
    (
        """
        x = " \\n
        foo \\n
        "\n
        """,
        """
        x = " \\n
        foo \\n
        "\n
        """,
        0
    ),
)


@pytest.mark.parametrize(('input_s', 'expected_output', 'expected_retval'), TESTS)
def test_rewrite(input_s, expected_output, expected_retval, tmpdir):
    tmpfile = tmpdir.join('file.txt')

    with open(tmpfile.strpath, 'w') as f:
        f.write(input_s)

    retval = main([tmpfile.strpath])
    assert tmpfile.read() == expected_output
    assert retval == expected_retval
