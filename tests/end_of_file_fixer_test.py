import io
import os.path

import pytest

from pre_commit_hooks.end_of_file_fixer import end_of_file_fixer
from pre_commit_hooks.end_of_file_fixer import fix_file


# Input, expected return value, expected output
TESTS = (
    (b'foo\n', 0, b'foo\n'),
    (b'', 0, b''),
    (b'\n\n', 1, b''),
    (b'\n\n\n\n', 1, b''),
    (b'foo', 1, b'foo\n'),
    (b'foo\n\n\n', 1, b'foo\n'),
    (b'\xe2\x98\x83', 1, b'\xe2\x98\x83\n'),
)


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_fix_file(input_s, expected_retval, output):
    file_obj = io.BytesIO()
    file_obj.write(input_s)
    ret = fix_file(file_obj)
    assert file_obj.getvalue() == output
    assert ret == expected_retval


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_integration(input_s, expected_retval, output, tmpdir):
    file_path = os.path.join(tmpdir.strpath, 'file.txt')

    with open(file_path, 'wb') as file_obj:
        file_obj.write(input_s)

    ret = end_of_file_fixer([file_path])
    file_output = open(file_path, 'rb').read()

    assert file_output == output
    assert ret == expected_retval
