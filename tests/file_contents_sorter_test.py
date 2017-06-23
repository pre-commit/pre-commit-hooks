import pytest

from pre_commit_hooks.file_contents_sorter import FAIL
from pre_commit_hooks.file_contents_sorter import main
from pre_commit_hooks.file_contents_sorter import parse_commandline_input
from pre_commit_hooks.file_contents_sorter import PASS


def _n(*strs):
    return b'\n'.join(strs) + b'\n'


# Input, expected return value, expected output
TESTS = (
    (b'', PASS, b''),
    (_n(b'lonesome'), PASS, _n(b'lonesome')),
    (b'missing_newline', PASS, b'missing_newline'),
    (_n(b'alpha', b'beta'), PASS, _n(b'alpha', b'beta')),
    (_n(b'beta', b'alpha'), FAIL, _n(b'alpha', b'beta')),
    (_n(b'C', b'c'), PASS, _n(b'C', b'c')),
    (_n(b'c', b'C'), FAIL, _n(b'C', b'c')),
    (_n(b'mag ical ', b' tre vor'), FAIL, _n(b' tre vor', b'mag ical ')),
    (_n(b'@', b'-', b'_', b'#'), FAIL, _n(b'#', b'-', b'@', b'_')),
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
