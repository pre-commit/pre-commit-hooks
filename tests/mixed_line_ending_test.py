import pytest

from pre_commit_hooks.mixed_line_ending import mixed_line_ending

# Input, expected return value, expected output
TESTS_FIX_AUTO = (
    # only 'LF'
    (b'foo\nbar\nbaz\n', 0, b'foo\nbar\nbaz\n'),
    # only 'CRLF'
    (b'foo\r\nbar\r\nbaz\r\n', 0, b'foo\r\nbar\r\nbaz\r\n'),
    # mixed with majority of 'LF'
    (b'foo\r\nbar\nbaz\n', 1, b'foo\nbar\nbaz\n'),
    # mixed with majority of 'CRLF'
    (b'foo\r\nbar\nbaz\r\n', 1, b'foo\r\nbar\r\nbaz\r\n'),
)


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'),
                         TESTS_FIX_AUTO)
def test_mixed_line_ending_fix_auto(input_s, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    ret = mixed_line_ending(('--fix=auto', '-vv', path.strpath))

    assert ret == expected_retval
    assert path.read() == output
