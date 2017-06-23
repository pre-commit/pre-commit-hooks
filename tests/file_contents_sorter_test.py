import pytest

from pre_commit_hooks.file_contents_sorter import FAIL
from pre_commit_hooks.file_contents_sorter import main
from pre_commit_hooks.file_contents_sorter import parse_commandline_input
from pre_commit_hooks.file_contents_sorter import PASS


# Input, expected return value, expected output
TESTS = (
    (b'', PASS, b''),
    (b'lonesome\n', PASS, b'lonesome\n'),
    (b'missing_newline', PASS, b'missing_newline'),
    (b'alpha\nbeta\n', PASS, b'alpha\nbeta\n'),
    (b'beta\nalpha\n', FAIL, b'alpha\nbeta\n'),
    (b'C\nc\n', PASS, b'C\nc\n'),
    (b'c\nC\n', FAIL, b'C\nc\n'),
    (b'mag ical \n tre vor\n', FAIL, b' tre vor\nmag ical \n'),
    (b'@\n-\n_\n#\n', FAIL, b'#\n-\n@\n_\n'),
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
