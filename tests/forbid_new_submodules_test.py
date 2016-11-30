from __future__ import absolute_import

import pytest
from pre_commit.util import cmd_output

from pre_commit_hooks.forbid_new_submodules import main


@pytest.yield_fixture
def git_dir_with_git_dir(tmpdir):
    with tmpdir.as_cwd():
        cmd_output('git', 'init', '.')
        cmd_output('git', 'commit', '-m', 'init', '--allow-empty')
        cmd_output('git', 'init', 'foo')
        with tmpdir.join('foo').as_cwd():
            cmd_output('git', 'commit', '-m', 'init', '--allow-empty')
        yield


@pytest.mark.parametrize(
    'cmd',
    (
        # Actually add the submodule
        ('git', 'submodule', 'add', './foo'),
        # Sneaky submodule add (that doesn't show up in .gitmodules)
        ('git', 'add', 'foo'),
    ),
)
def test_main_new_submodule(git_dir_with_git_dir, capsys, cmd):
    cmd_output(*cmd)
    assert main() == 1
    out, _ = capsys.readouterr()
    assert out.startswith('foo: new submodule introduced\n')


def test_main_no_new_submodule(git_dir_with_git_dir):
    open('test.py', 'a+').close()
    cmd_output('git', 'add', 'test.py')
    assert main() == 0
