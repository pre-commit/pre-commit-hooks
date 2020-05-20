import io

import pytest

from pre_commit_hooks.end_of_file_fixer import fix_file
from pre_commit_hooks.end_of_file_fixer import main


# Input, expected return value, expected output
TESTS = (
    (b'foo\n', 0, b'foo\n'),
    (b'', 0, b''),
    (b'\n\n', 1, b''),
    (b'\n\n\n\n', 1, b''),
    (b'foo', 1, b'foo\n'),
    (b'foo\n\n\n', 1, b'foo\n'),
    (b'\xe2\x98\x83', 1, b'\xe2\x98\x83\n'),
    (b'foo\r\n', 0, b'foo\r\n'),
    (b'foo\r\n\r\n\r\n', 1, b'foo\r\n'),
    (b'foo\r', 0, b'foo\r'),
    (b'foo\r\r\r\r', 1, b'foo\r'),
)


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_fix_file(input_s, expected_retval, output):
    file_obj = io.BytesIO(input_s)
    ret = fix_file(file_obj)
    assert file_obj.getvalue() == output
    assert ret == expected_retval


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_integration(input_s, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)

    ret = main([str(path)])
    file_output = path.read_binary()

    assert file_output == output
    assert ret == expected_retval
