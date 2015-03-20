from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.trailing_whitespace_fixer import fix_trailing_whitespace
from testing.util import cwd


def test_fixes_trailing_whitespace(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('foo.py', 'foo \nbar \n'),
                ('bar.py', 'bar\t\nbaz\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no cover (26 coverage bug)

        ret = fix_trailing_whitespace(['foo.py', 'bar.py'])
        assert ret == 1

        for filename, after_contents in (
                ('foo.py', 'foo\nbar\n'),
                ('bar.py', 'bar\nbaz\n'),
        ):
            assert open(filename).read() == after_contents


def test_returns_zero_for_no_changes():
    assert fix_trailing_whitespace([__file__]) == 0
