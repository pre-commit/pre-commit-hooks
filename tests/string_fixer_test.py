import textwrap

import pytest

from pre_commit_hooks.string_fixer import main

TESTS = (
    # Base cases
    ("''", "''", 0),
    ('""', "''", 1),
    (r'"\'"', r'"\'"', 0),
    (r'"\""', r'"\""', 0),
    (r"'\"\"'", r"'\"\"'", 0),
    # String somewhere in the line
    ('x = "foo"', "x = 'foo'", 1),
    # Test escaped characters
    (r'"\'"', r'"\'"', 0),
    # Docstring
    ('""" Foo """', '""" Foo """', 0),
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
        1,
    ),
    ('"foo""bar"', "'foo''bar'", 1),
)


@pytest.mark.parametrize(('input_s', 'output', 'expected_retval'), TESTS)
def test_rewrite(input_s, output, expected_retval, tmpdir):
    path = tmpdir.join('file.py')
    path.write(input_s)
    retval = main([str(path)])
    assert path.read() == output
    assert retval == expected_retval


def test_rewrite_crlf(tmpdir):
    f = tmpdir.join('f.py')
    f.write_binary(b'"foo"\r\n"bar"\r\n')
    assert main((str(f),))
    assert f.read_binary() == b"'foo'\r\n'bar'\r\n"
