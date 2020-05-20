import os

import pytest

from pre_commit_hooks.sort_simple_yaml import first_key
from pre_commit_hooks.sort_simple_yaml import main
from pre_commit_hooks.sort_simple_yaml import parse_block
from pre_commit_hooks.sort_simple_yaml import parse_blocks
from pre_commit_hooks.sort_simple_yaml import sort

RETVAL_GOOD = 0
RETVAL_BAD = 1
TEST_SORTS = [
    (
        ['c: true', '', 'b: 42', 'a: 19'],
        ['b: 42', 'a: 19', '', 'c: true'],
        RETVAL_BAD,
    ),

    (
        ['# i am', '# a header', '', 'c: true', '', 'b: 42', 'a: 19'],
        ['# i am', '# a header', '', 'b: 42', 'a: 19', '', 'c: true'],
        RETVAL_BAD,
    ),

    (
        ['# i am', '# a header', '', 'already: sorted', '', 'yup: i am'],
        ['# i am', '# a header', '', 'already: sorted', '', 'yup: i am'],
        RETVAL_GOOD,
    ),

    (
        ['# i am', '# a header'],
        ['# i am', '# a header'],
        RETVAL_GOOD,
    ),
]


@pytest.mark.parametrize('bad_lines,good_lines,retval', TEST_SORTS)
def test_integration_good_bad_lines(tmpdir, bad_lines, good_lines, retval):
    file_path = os.path.join(str(tmpdir), 'foo.yaml')

    with open(file_path, 'w') as f:
        f.write('\n'.join(bad_lines) + '\n')

    assert main([file_path]) == retval

    with open(file_path) as f:
        assert [line.rstrip() for line in f.readlines()] == good_lines


def test_parse_header():
    lines = ['# some header', '# is here', '', 'this is not a header']
    assert parse_block(lines, header=True) == ['# some header', '# is here']
    assert lines == ['', 'this is not a header']

    lines = ['this is not a header']
    assert parse_block(lines, header=True) == []
    assert lines == ['this is not a header']


def test_parse_block():
    # a normal block
    lines = ['a: 42', 'b: 17', '', 'c: 19']
    assert parse_block(lines) == ['a: 42', 'b: 17']
    assert lines == ['', 'c: 19']

    # a block at the end
    lines = ['c: 19']
    assert parse_block(lines) == ['c: 19']
    assert lines == []

    # no block
    lines = []
    assert parse_block(lines) == []
    assert lines == []


def test_parse_blocks():
    # normal blocks
    lines = ['a: 42', 'b: 17', '', 'c: 19']
    assert parse_blocks(lines) == [['a: 42', 'b: 17'], ['c: 19']]
    assert lines == []

    # a single block
    lines = ['a: 42', 'b: 17']
    assert parse_blocks(lines) == [['a: 42', 'b: 17']]
    assert lines == []

    # no blocks
    lines = []
    assert parse_blocks(lines) == []
    assert lines == []


def test_first_key():
    # first line
    lines = ['a: 42', 'b: 17', '', 'c: 19']
    assert first_key(lines) == 'a: 42'

    # second line
    lines = ['# some comment', 'a: 42', 'b: 17', '', 'c: 19']
    assert first_key(lines) == 'a: 42'

    # second line with quotes
    lines = ['# some comment', '"a": 42', 'b: 17', '', 'c: 19']
    assert first_key(lines) == 'a": 42'

    # no lines (not a real situation)
    lines = []
    assert first_key(lines) == ''


@pytest.mark.parametrize('bad_lines,good_lines,_', TEST_SORTS)
def test_sort(bad_lines, good_lines, _):
    assert sort(bad_lines) == good_lines
