from plumbum import local

from pre_commit_hooks.trailing_whitespace_fixer import fix_trailing_whitespace


def test_fixes_trailing_whitespace(tmpdir):
    with local.cwd(tmpdir.strpath):
        for filename, contents in (
            ('foo.py', 'foo \nbar \n'),
            ('bar.py', 'bar\t\nbaz\t\n'),
        ):
            with open(filename, 'w') as f:
                f.write(contents)  # pragma: no cover (python 2.6 coverage bug)

        ret = fix_trailing_whitespace(['foo.py', 'bar.py'])
        assert ret == 1

        for filename, after_contents in (
            ('foo.py', 'foo\nbar\n'),
            ('bar.py', 'bar\nbaz\n'),
        ):
            assert open(filename).read() == after_contents


def test_returns_zero_for_no_changes():
    assert fix_trailing_whitespace([__file__]) == 0
