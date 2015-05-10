from __future__ import absolute_import
from __future__ import unicode_literals

import sys

import pytest

from pre_commit_hooks.trailing_whitespace_fixer import fix_trailing_whitespace
from testing.util import cwd


def test_fixes_trailing_whitespace(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('foo.py', 'foo \nbar \n'),
                ('bar.py', 'bar\t\nbaz\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['foo.py', 'bar.py'])
        assert ret == 1

        for filename, after_contents in (
                ('foo.py', 'foo\nbar\n'),
                ('bar.py', 'bar\nbaz\n'),
        ):
            assert open(filename).read() == after_contents


# filename, expected input, expected output
# pylint: disable=bad-whitespace
MD_TESTS_1 = (
    ('foo.md',        'foo  \nbar \n  ',         'foo  \nbar\n\n'),
    ('bar.Markdown',  'bar   \nbaz\t\n\t\n',     'bar  \nbaz\n\n'),
    ('.md',           'baz   \nquux  \t\n\t\n',  'baz\nquux\n\n'),
    ('txt',           'foo   \nbaz \n\t\n',      'foo\nbaz\n\n'),
)
# pylint: enable=bad-whitespace


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_1)
def test_fixes_trailing_markdown_whitespace(filename, input_s, output, tmpdir):
    with cwd(tmpdir.strpath):
        with open(filename, 'w') as file_obj:
            file_obj.write(input_s)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace([filename])
        assert ret == 1
        assert open(filename).read() == output


# filename, expected input, expected output
# pylint: disable=bad-whitespace
MD_TESTS_2 = (
    ('foo.txt',       'foo  \nbar \n  \n',       'foo  \nbar\n\n'),
    ('bar.Markdown',  'bar   \nbaz\t\n\t\n',     'bar  \nbaz\n\n'),
    ('bar.MD',        'bar   \nbaz\t   \n\t\n',  'bar  \nbaz\n\n'),
    ('.txt',          'baz   \nquux  \t\n\t\n',  'baz\nquux\n\n'),
    ('txt',           'foo   \nbaz \n\t\n',      'foo\nbaz\n\n'),
)
# pylint: enable=bad-whitespace


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_2)
def test_markdown_linebreak_ext_opt(filename, input_s, output, tmpdir):
    with cwd(tmpdir.strpath):
        with open(filename, 'w') as file_obj:
            file_obj.write(input_s)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['--markdown-linebreak-ext=TxT',
                                       filename])
        assert ret == 1
        assert open(filename).read() == output


# filename, expected input, expected output
# pylint: disable=bad-whitespace
MD_TESTS_3 = (
    ('foo.baz',       'foo  \nbar \n  ',         'foo  \nbar\n\n'),
    ('bar',           'bar   \nbaz\t\n\t\n',     'bar  \nbaz\n\n'),
)
# pylint: enable=bad-whitespace


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_3)
def test_markdown_linebreak_ext_opt_all(filename, input_s, output, tmpdir):
    with cwd(tmpdir.strpath):
        with open(filename, 'w') as file_obj:
            file_obj.write(input_s)  # pragma: no branch (26 coverage bug)

        # need to make sure filename is not treated as argument to option
        ret = fix_trailing_whitespace(['--markdown-linebreak-ext=*',
                                       filename])
        assert ret == 1
        assert open(filename).read() == output


@pytest.mark.parametrize(('arg'), ('--', 'a.b', 'a/b'))
def test_markdown_linebreak_ext_badopt(arg):
    try:
        ret = fix_trailing_whitespace(['--markdown-linebreak-ext', arg])
    except SystemExit:
        ret = sys.exc_info()[1].code
    finally:
        assert ret == 2


# filename, expected input, expected output
# pylint: disable=bad-whitespace
MD_TESTS_4 = (
    ('bar.md',        'bar   \nbaz\t   \n\t\n',  'bar\nbaz\n\n'),
    ('bar.markdown',  'baz   \nquux  \n',        'baz\nquux\n'),
)
# pylint: enable=bad-whitespace


@pytest.mark.parametrize(('filename', 'input_s', 'output'), MD_TESTS_4)
def test_no_markdown_linebreak_ext_opt(filename, input_s, output, tmpdir):
    with cwd(tmpdir.strpath):
        with open(filename, 'w') as file_obj:
            file_obj.write(input_s)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['--no-markdown-linebreak-ext', filename])
        assert ret == 1
        assert open(filename).read() == output


def test_returns_zero_for_no_changes():
    assert fix_trailing_whitespace([__file__]) == 0
