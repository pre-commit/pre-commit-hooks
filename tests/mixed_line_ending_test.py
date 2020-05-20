import pytest

from pre_commit_hooks.mixed_line_ending import main


@pytest.mark.parametrize(
    ('input_s', 'output'),
    (
        # mixed with majority of 'LF'
        (b'foo\r\nbar\nbaz\n', b'foo\nbar\nbaz\n'),
        # mixed with majority of 'CRLF'
        (b'foo\r\nbar\nbaz\r\n', b'foo\r\nbar\r\nbaz\r\n'),
        # mixed with majority of 'CR'
        (b'foo\rbar\nbaz\r', b'foo\rbar\rbaz\r'),
        # mixed with as much 'LF' as 'CRLF'
        (b'foo\r\nbar\n', b'foo\nbar\n'),
        # mixed with as much 'LF' as 'CR'
        (b'foo\rbar\n', b'foo\nbar\n'),
        # mixed with as much 'CRLF' as 'CR'
        (b'foo\r\nbar\r', b'foo\r\nbar\r\n'),
        # mixed with as much 'CRLF' as 'LF' as 'CR'
        (b'foo\r\nbar\nbaz\r', b'foo\nbar\nbaz\n'),
    ),
)
def test_mixed_line_ending_fixes_auto(input_s, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)
    ret = main((str(path),))

    assert ret == 1
    assert path.read_binary() == output


def test_non_mixed_no_newline_end_of_file(tmpdir):
    path = tmpdir.join('f.txt')
    path.write_binary(b'foo\nbar\nbaz')
    assert not main((str(path),))
    # the hook *could* fix the end of the file, but leaves it alone
    # this is mostly to document the current behaviour
    assert path.read_binary() == b'foo\nbar\nbaz'


def test_mixed_no_newline_end_of_file(tmpdir):
    path = tmpdir.join('f.txt')
    path.write_binary(b'foo\r\nbar\nbaz')
    assert main((str(path),))
    # the hook rewrites the end of the file, this is slightly inconsistent
    # with the non-mixed case but I think this is the better behaviour
    # this is mostly to document the current behaviour
    assert path.read_binary() == b'foo\nbar\nbaz\n'


@pytest.mark.parametrize(
    ('fix_option', 'input_s'),
    (
        # All --fix=auto with uniform line endings should be ok
        ('--fix=auto', b'foo\r\nbar\r\nbaz\r\n'),
        ('--fix=auto', b'foo\rbar\rbaz\r'),
        ('--fix=auto', b'foo\nbar\nbaz\n'),
        # --fix=crlf with crlf endings
        ('--fix=crlf', b'foo\r\nbar\r\nbaz\r\n'),
        # --fix=lf with lf endings
        ('--fix=lf', b'foo\nbar\nbaz\n'),
    ),
)
def test_line_endings_ok(fix_option, input_s, tmpdir, capsys):
    path = tmpdir.join('input.txt')
    path.write_binary(input_s)
    ret = main((fix_option, str(path)))

    assert ret == 0
    assert path.read_binary() == input_s
    out, _ = capsys.readouterr()
    assert out == ''


def test_no_fix_does_not_modify(tmpdir, capsys):
    path = tmpdir.join('input.txt')
    contents = b'foo\r\nbar\rbaz\nwomp\n'
    path.write_binary(contents)
    ret = main(('--fix=no', str(path)))

    assert ret == 1
    assert path.read_binary() == contents
    out, _ = capsys.readouterr()
    assert out == f'{path}: mixed line endings\n'


def test_fix_lf(tmpdir, capsys):
    path = tmpdir.join('input.txt')
    path.write_binary(b'foo\r\nbar\rbaz\n')
    ret = main(('--fix=lf', str(path)))

    assert ret == 1
    assert path.read_binary() == b'foo\nbar\nbaz\n'
    out, _ = capsys.readouterr()
    assert out == f'{path}: fixed mixed line endings\n'


def test_fix_crlf(tmpdir):
    path = tmpdir.join('input.txt')
    path.write_binary(b'foo\r\nbar\rbaz\n')
    ret = main(('--fix=crlf', str(path)))

    assert ret == 1
    assert path.read_binary() == b'foo\r\nbar\r\nbaz\r\n'


def test_fix_lf_all_crlf(tmpdir):
    """Regression test for #239"""
    path = tmpdir.join('input.txt')
    path.write_binary(b'foo\r\nbar\r\n')
    ret = main(('--fix=lf', str(path)))

    assert ret == 1
    assert path.read_binary() == b'foo\nbar\n'
