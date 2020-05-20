import pytest

from pre_commit_hooks.trailing_whitespace_fixer import main


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('foo \nbar \n', 'foo\nbar\n'),
        ('bar\t\nbaz\t\n', 'bar\nbaz\n'),
    ),
)
def test_fixes_trailing_whitespace(input_s, expected, tmpdir):
    path = tmpdir.join('file.md')
    path.write(input_s)
    assert main((str(path),)) == 1
    assert path.read() == expected


def test_ok_no_newline_end_of_file(tmpdir):
    filename = tmpdir.join('f')
    filename.write_binary(b'foo\nbar')
    ret = main((str(filename),))
    assert filename.read_binary() == b'foo\nbar'
    assert ret == 0


def test_ok_with_dos_line_endings(tmpdir):
    filename = tmpdir.join('f')
    filename.write_binary(b'foo\r\nbar\r\nbaz\r\n')
    ret = main((str(filename),))
    assert filename.read_binary() == b'foo\r\nbar\r\nbaz\r\n'
    assert ret == 0


@pytest.mark.parametrize('ext', ('md', 'Md', '.md', '*'))
def test_fixes_markdown_files(tmpdir, ext):
    path = tmpdir.join('test.md')
    path.write(
        'foo  \n'  # leaves alone
        'bar \n'  # less than two so it is removed
        'baz    \n'  # more than two so it becomes two spaces
        '\t\n'  # trailing tabs are stripped anyway
        '\n  ',  # whitespace at the end of the file is removed
    )
    ret = main((str(path), f'--markdown-linebreak-ext={ext}'))
    assert ret == 1
    assert path.read() == (
        'foo  \n'
        'bar\n'
        'baz  \n'
        '\n'
        '\n'
    )


@pytest.mark.parametrize('arg', ('--', 'a.b', 'a/b', ''))
def test_markdown_linebreak_ext_badopt(arg):
    with pytest.raises(SystemExit) as excinfo:
        main(['--markdown-linebreak-ext', arg])
    assert excinfo.value.code == 2


def test_prints_warning_with_no_markdown_ext(capsys, tmpdir):
    f = tmpdir.join('f').ensure()
    assert main((str(f), '--no-markdown-linebreak-ext')) == 0
    out, _ = capsys.readouterr()
    assert out == '--no-markdown-linebreak-ext now does nothing!\n'


def test_preserve_non_utf8_file(tmpdir):
    non_utf8_bytes_content = b'<a>\xe9 \n</a>\n'
    path = tmpdir.join('file.txt')
    path.write_binary(non_utf8_bytes_content)
    ret = main([str(path)])
    assert ret == 1
    assert path.size() == (len(non_utf8_bytes_content) - 1)


def test_custom_charset_change(tmpdir):
    # strip spaces only, no tabs
    path = tmpdir.join('file.txt')
    path.write('\ta \t \n')
    ret = main([str(path), '--chars', ' '])
    assert ret == 1
    assert path.read() == '\ta \t\n'


def test_custom_charset_no_change(tmpdir):
    path = tmpdir.join('file.txt')
    path.write('\ta \t\n')
    ret = main([str(path), '--chars', ' '])
    assert ret == 0


def test_markdown_with_custom_charset(tmpdir):
    path = tmpdir.join('file.md')
    path.write('\ta \t   \n')
    ret = main([str(path), '--chars', ' ', '--markdown-linebreak-ext', '*'])
    assert ret == 1
    assert path.read() == '\ta \t  \n'
