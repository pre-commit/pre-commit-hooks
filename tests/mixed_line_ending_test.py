import pytest

from pre_commit_hooks.mixed_line_ending import mixed_line_ending

# Input, expected return value, expected output
TESTS_FIX_AUTO = (
    # only 'LF'
    (b'foo\nbar\nbaz\n', 0, b'foo\nbar\nbaz\n'),
    # only 'CRLF'
    (b'foo\r\nbar\r\nbaz\r\n', 0, b'foo\r\nbar\r\nbaz\r\n'),
    # only 'CR'
    (b'foo\rbar\rbaz\r', 0, b'foo\rbar\rbaz\r'),
    # mixed with majority of 'LF'
    (b'foo\r\nbar\nbaz\n', 1, b'foo\nbar\nbaz\n'),
    # mixed with majority of 'CRLF'
    (b'foo\r\nbar\nbaz\r\n', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # mixed with majority of 'CR'
    (b'foo\rbar\nbaz\r', 1, b'foo\rbar\rbaz\r'),
    # mixed with as much 'LF' as 'CRLF'
    (b'foo\r\nbar\nbaz', 1, b'foo\r\nbar\nbaz'),
    # mixed with as much 'LF' as 'CR'
    (b'foo\rbar\nbaz', 1, b'foo\rbar\nbaz'),
    # mixed with as much 'CRLF' as 'CR'
    (b'foo\r\nbar\nbaz', 1, b'foo\r\nbar\nbaz'),
    # mixed with as much 'CRLF' as 'LF' as 'CR'
    (b'foo\r\nbar\nbaz\r', 1, b'foo\r\nbar\nbaz\r'),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_retval', 'output'),
    TESTS_FIX_AUTO,
)
def test_mixed_line_ending_fix_auto(input_s, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    ret = mixed_line_ending(('--fix=auto', path.strpath))

    assert ret == expected_retval
    assert path.read_binary() == output


# Input, expected return value, expected output
TESTS_NO_FIX = (
    # only 'LF'
    (b'foo\nbar\nbaz\n', 0, b'foo\nbar\nbaz\n'),
    # only 'CRLF'
    (b'foo\r\nbar\r\nbaz\r\n', 0, b'foo\r\nbar\r\nbaz\r\n'),
    # only 'CR'
    (b'foo\rbar\rbaz\r', 0, b'foo\rbar\rbaz\r'),
    # mixed with majority of 'LF'
    (b'foo\r\nbar\nbaz\n', 1, b'foo\r\nbar\nbaz\n'),
    # mixed with majority of 'CRLF'
    (b'foo\r\nbar\nbaz\r\n', 1, b'foo\r\nbar\nbaz\r\n'),
    # mixed with majority of 'CR'
    (b'foo\rbar\nbaz\r', 1, b'foo\rbar\nbaz\r'),
    # mixed with as much 'LF' as 'CR'
    (b'foo\rbar\nbaz', 0, b'foo\rbar\nbaz'),
    # mixed with as much 'CRLF' as 'CR'
    (b'foo\r\nbar\nbaz', 0, b'foo\r\nbar\nbaz'),
    # mixed with as much 'CRLF' as 'LF' as 'CR'
    (b'foo\r\nbar\nbaz\r', 0, b'foo\r\nbar\nbaz\r'),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_retval', 'output'),
    TESTS_NO_FIX,
)
def test_detect_mixed_line_ending(input_s, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    ret = mixed_line_ending(('--fix=no', path.strpath))

    assert ret == expected_retval
    assert path.read_binary() == output


# Input, expected return value, expected output
TESTS_FIX_FORCE_LF = (
    # only 'LF'
    (b'foo\nbar\nbaz\n', 1, b'foo\nbar\nbaz\n'),
    # only 'CRLF'
    (b'foo\r\nbar\r\nbaz\r\n', 1, b'foo\nbar\nbaz\n'),
    # only 'CR'
    (b'foo\rbar\rbaz\r', 1, b'foo\nbar\nbaz\n'),
    # mixed with majority of 'LF'
    (b'foo\r\nbar\nbaz\n', 1, b'foo\nbar\nbaz\n'),
    # mixed with majority of 'CRLF'
    (b'foo\r\nbar\nbaz\r\n', 1, b'foo\nbar\nbaz\n'),
    # mixed with majority of 'CR'
    (b'foo\rbar\nbaz\r', 1, b'foo\nbar\nbaz\n'),
    # mixed with as much 'LF' as 'CR'
    (b'foo\rbar\nbaz', 1, b'foo\nbar\nbaz'),
    # mixed with as much 'CRLF' as 'CR'
    (b'foo\r\nbar\nbaz', 1, b'foo\nbar\nbaz'),
    # mixed with as much 'CRLF' as 'LF' as 'CR'
    (b'foo\r\nbar\nbaz\r', 1, b'foo\nbar\nbaz\n'),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_retval', 'output'),
    TESTS_FIX_FORCE_LF,
)
def test_mixed_line_ending_fix_force_lf(
    input_s, expected_retval, output,
    tmpdir,
):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    ret = mixed_line_ending(('--fix=lf', path.strpath))

    assert ret == expected_retval
    assert path.read_binary() == output


# Input, expected return value, expected output
TESTS_FIX_FORCE_CRLF = (
    # only 'LF'
    (b'foo\nbar\nbaz\n', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # only 'CRLF'
    (b'foo\r\nbar\r\nbaz\r\n', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # only 'CR'
    (b'foo\rbar\rbaz\r', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # mixed with majority of 'LF'
    (b'foo\r\nbar\nbaz\n', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # mixed with majority of 'CRLF'
    (b'foo\r\nbar\nbaz\r\n', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # mixed with majority of 'CR'
    (b'foo\rbar\nbaz\r', 1, b'foo\r\nbar\r\nbaz\r\n'),
    # mixed with as much 'LF' as 'CR'
    (b'foo\rbar\nbaz', 1, b'foo\r\nbar\r\nbaz'),
    # mixed with as much 'CRLF' as 'CR'
    (b'foo\r\nbar\nbaz', 1, b'foo\r\nbar\r\nbaz'),
    # mixed with as much 'CRLF' as 'LF' as 'CR'
    (b'foo\r\nbar\nbaz\r', 1, b'foo\r\nbar\r\nbaz\r\n'),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_retval', 'output'),
    TESTS_FIX_FORCE_CRLF,
)
def test_mixed_line_ending_fix_force_crlf(
    input_s, expected_retval, output,
    tmpdir,
):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    ret = mixed_line_ending(('--fix=crlf', path.strpath))

    assert ret == expected_retval
    assert path.read_binary() == output


def test_check_filenames():
    with pytest.raises(IOError):
        mixed_line_ending(['/dev/null'])
