from argparse import ArgumentError

import pytest

from pre_commit_hooks.file_contents_sorter import FAIL
from pre_commit_hooks.file_contents_sorter import main
from pre_commit_hooks.file_contents_sorter import parse_commandline_input
from pre_commit_hooks.file_contents_sorter import PASS
from pre_commit_hooks.file_contents_sorter import sort_file_contents


def _n(*strs):
    return b'\n'.join(strs) + '\n'


# Input, expected return value, expected output
TESTS = (
    (b'', PASS, b''),
    (_n('lonesome'), PASS, _n('lonesome')),
    (b'missing_newline', PASS, b'missing_newline'),
    (_n('alpha', 'beta'), PASS, _n('alpha', 'beta')),
    (_n('beta', 'alpha'), FAIL, _n('alpha', 'beta')),
    (_n('C', 'c'), PASS, _n('C', 'c')),
    (_n('c', 'C'), FAIL, _n('C', 'c')),
    (_n('mag ical ', ' tre vor'), FAIL, _n(' tre vor', 'mag ical ')),
    (_n('@', '-', '_', '#'), FAIL, _n('#', '-', '@', '_')),
)


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_integration(input_s, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)

    output_retval = main([path.strpath])

    assert path.read_binary() == output
    assert output_retval == expected_retval


def test_parse_commandline_input_errors_without_args():
    with pytest.raises(SystemExit):
        parse_commandline_input([])

@pytest.mark.parametrize(
    ('filename_list'), 
    (
        ['filename1'], 
        ['filename1', 'filename2'],
    )
)
def test_parse_commandline_input_success(filename_list):
    args = parse_commandline_input(filename_list)
    assert args.filenames == filename_list