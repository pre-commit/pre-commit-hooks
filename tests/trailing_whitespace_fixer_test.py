from __future__ import absolute_import
from __future__ import unicode_literals

import sys

import pytest

from pre_commit_hooks.trailing_whitespace_fixer import fix_trailing_whitespace


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('foo \nbar \n', 'foo\nbar\n'),
        ('bar\t\nbaz\t\n', 'bar\nbaz\n'),
    ),
)
def test_fixes_trailing_whitespace(input_s, expected, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    assert fix_trailing_whitespace((path.strpath,)) == 1
    assert path.read() == expected


# filename, expected input, expected output
MD_TESTS_1 = (
    ('foo.md', 'foo  \nbar \n  ', 'foo  \nbar\n\n'),
    ('bar.Markdown', 'bar   \nbaz\t\n\t\n', 'bar  \nbaz\n\n'),
    ('.md', 'baz   \nquux  \t\n\t\n', 'baz\nquux\n\n'),
    ('txt', 'foo   \nbaz \n\t\n', 'foo\nbaz\n\n'),
)


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_1)
def test_fixes_trailing_markdown_whitespace(filename, input_s, output, tmpdir):
    path = tmpdir.join(filename)
    path.write(input_s)
    ret = fix_trailing_whitespace([path.strpath])
    assert ret == 1
    assert path.read() == output


# filename, expected input, expected output
MD_TESTS_2 = (
    ('foo.txt', 'foo  \nbar \n  \n', 'foo  \nbar\n\n'),
    ('bar.Markdown', 'bar   \nbaz\t\n\t\n', 'bar  \nbaz\n\n'),
    ('bar.MD', 'bar   \nbaz\t   \n\t\n', 'bar  \nbaz\n\n'),
    ('.txt', 'baz   \nquux  \t\n\t\n', 'baz\nquux\n\n'),
    ('txt', 'foo   \nbaz \n\t\n', 'foo\nbaz\n\n'),
)


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_2)
def test_markdown_linebreak_ext_opt(filename, input_s, output, tmpdir):
    path = tmpdir.join(filename)
    path.write(input_s)
    ret = fix_trailing_whitespace((
        '--markdown-linebreak-ext=TxT', path.strpath
    ))
    assert ret == 1
    assert path.read() == output


# filename, expected input, expected output
MD_TESTS_3 = (
    ('foo.baz', 'foo  \nbar \n  ', 'foo  \nbar\n\n'),
    ('bar', 'bar   \nbaz\t\n\t\n', 'bar  \nbaz\n\n'),
)


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_3)
def test_markdown_linebreak_ext_opt_all(filename, input_s, output, tmpdir):
    path = tmpdir.join(filename)
    path.write(input_s)
    # need to make sure filename is not treated as argument to option
    ret = fix_trailing_whitespace([
        '--markdown-linebreak-ext=*', path.strpath,
    ])
    assert ret == 1
    assert path.read() == output


@pytest.mark.parametrize(('arg'), ('--', 'a.b', 'a/b'))
def test_markdown_linebreak_ext_badopt(arg):
    with pytest.raises(SystemExit) as excinfo:
        fix_trailing_whitespace(['--markdown-linebreak-ext', arg])
    assert excinfo.value.code == 2


# filename, expected input, expected output
MD_TESTS_4 = (
    ('bar.md', 'bar   \nbaz\t   \n\t\n', 'bar\nbaz\n\n'),
    ('bar.markdown', 'baz   \nquux  \n', 'baz\nquux\n'),
)


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_4)
def test_no_markdown_linebreak_ext_opt(filename, input_s, output, tmpdir):
    path = tmpdir.join(filename)
    path.write(input_s)
    ret = fix_trailing_whitespace(['--no-markdown-linebreak-ext', path.strpath])
    assert ret == 1
    assert path.read() == output


def test_returns_zero_for_no_changes():
    assert fix_trailing_whitespace([__file__]) == 0


def test_preserve_non_utf8_file(tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(b'<a>\xe9 \n</a>')
    ret = fix_trailing_whitespace([path.strpath])
    assert ret == (1 if sys.version_info[0] < 3 else 0)  # a UnicodeDecodeError is only triggered in Python 3
    assert path.size() > 0
