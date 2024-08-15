from __future__ import annotations

import textwrap

import pytest

from pre_commit_hooks.string_fixer import main

TESTS = (
    # Base cases
    ("''", "''", False, 0),
    ("''", '""', True, 1),
    ('""', "''", False, 1),
    ('""', '""', True, 0),
    (r'"\'"', r'"\'"', False, 0),
    (r'"\""', r'"\""', False, 0),
    (r"'\"\"'", r"'\"\"'", False, 0),
    # String somewhere in the line
    ('x = "foo"', "x = 'foo'", False, 1),
    ("x = 'foo'", 'x = "foo"', True, 1),
    # Test escaped characters
    (r'"\'"', r'"\'"', False, 0),
    # Docstring
    ('""" Foo """', '""" Foo """', False, 0),
    (
        textwrap.dedent(
            """
        x = " \\
        foo \\
        "\n
        """,
        ),
        textwrap.dedent(
            """
        x = ' \\
        foo \\
        '\n
        """,
        ),
        False,
        1,
    ),
    (
        textwrap.dedent(
            """
        x = ' \\
        foo \\
        '\n
        """,
        ),
        textwrap.dedent(
            """
        x = " \\
        foo \\
        "\n
        """,
        ),
        True,
        1,
    ),
    ('"foo""bar"', "'foo''bar'", False, 1),
    ("'foo''bar'", '"foo""bar"', True, 1),
    pytest.param(
        "f'hello{\"world\"}'",
        "f'hello{\"world\"}'",
        False,
        0,
        id='ignore nested fstrings',
    ),
)


@pytest.mark.parametrize(
    ('input_s', 'output', 'reversed_case', 'expected_retval'), TESTS
)
def test_rewrite(input_s, output, reversed_case, expected_retval, tmpdir):
    path = tmpdir.join('file.py')
    path.write(input_s)

    argv = [str(path)]
    if reversed_case:
        argv.append("--replace-single-quotes")
    retval = main(argv)

    assert path.read() == output
    assert retval == expected_retval


def test_rewrite_crlf(tmpdir):
    f = tmpdir.join('f.py')
    f.write_binary(b'"foo"\r\n"bar"\r\n')
    assert main((str(f),))
    assert f.read_binary() == b"'foo'\r\n'bar'\r\n"
