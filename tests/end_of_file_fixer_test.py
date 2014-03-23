
import cStringIO
import os.path
import pytest

from pre_commit_hooks.end_of_file_fixer import end_of_file_fixer
from pre_commit_hooks.end_of_file_fixer import fix_file


# Input, expected return value, expected output
TESTS = (
    ('foo\n', 0, 'foo\n'),
    ('', 0, ''),
    ('\n\n', 1, ''),
    ('\n\n\n\n', 1, ''),
    ('foo', 1, 'foo\n'),
    ('foo\n\n\n', 1, 'foo\n'),
    ('\xe2\x98\x83', 1, '\xe2\x98\x83\n'),
)


@pytest.mark.parametrize(('input', 'expected_retval', 'output'), TESTS)
def test_fix_file(input, expected_retval, output):
    file_obj = cStringIO.StringIO()
    file_obj.write(input)
    ret = fix_file(file_obj)
    assert file_obj.getvalue() == output
    assert ret == expected_retval


@pytest.mark.parametrize(('input', 'expected_retval', 'output'), TESTS)
def test_integration(input, expected_retval, output, tmpdir):
    file_path = os.path.join(tmpdir.strpath, 'file.txt')

    with open(file_path, 'w') as file_obj:
        file_obj.write(input)

    ret = end_of_file_fixer([file_path])
    file_output = open(file_path, 'r').read()

    assert file_output == output
    assert ret == expected_retval
