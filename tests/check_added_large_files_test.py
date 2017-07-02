from __future__ import absolute_import
from __future__ import unicode_literals

import subprocess

import pytest

from pre_commit_hooks.check_added_large_files import find_large_added_files
from pre_commit_hooks.check_added_large_files import main
from pre_commit_hooks.util import cmd_output


def test_nothing_added(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert find_large_added_files(['f.py'], 0) == 0


def test_adding_something(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        # Should fail with max size of 0
        assert find_large_added_files(['f.py'], 0) == 1


def test_add_something_giant(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write('a' * 10000)

        # Should not fail when not added
        assert find_large_added_files(['f.py'], 0) == 0

        cmd_output('git', 'add', 'f.py')

        # Should fail with strict bound
        assert find_large_added_files(['f.py'], 0) == 1

        # Should also fail with actual bound
        assert find_large_added_files(['f.py'], 9) == 1

        # Should pass with higher bound
        assert find_large_added_files(['f.py'], 10) == 0


def test_added_file_not_in_pre_commits_list(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        # Should pass even with a size of 0
        assert find_large_added_files(['g.py'], 0) == 0


def test_integration(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert main(argv=[]) == 0

        temp_git_dir.join('f.py').write('a' * 10000)
        cmd_output('git', 'add', 'f.py')

        # Should not fail with default
        assert main(argv=['f.py']) == 0

        # Should fail with --maxkb
        assert main(argv=['--maxkb', '9', 'f.py']) == 1


def has_gitlfs():
    output = cmd_output('git', 'lfs', retcode=None, stderr=subprocess.STDOUT)
    return 'git lfs status' in output


xfailif_no_gitlfs = pytest.mark.xfail(
    not has_gitlfs(), reason='This test requires git-lfs',
)


@xfailif_no_gitlfs
def test_allows_gitlfs(temp_git_dir):  # pragma: no cover
    with temp_git_dir.as_cwd():
        cmd_output('git', 'lfs', 'install')
        temp_git_dir.join('f.py').write('a' * 10000)
        cmd_output('git', 'lfs', 'track', 'f.py')
        cmd_output('git', 'add', '--', '.')
        # Should succeed
        assert main(('--maxkb', '9', 'f.py')) == 0


@xfailif_no_gitlfs
def test_moves_with_gitlfs(temp_git_dir):  # pragma: no cover
    with temp_git_dir.as_cwd():
        cmd_output('git', 'lfs', 'install')
        cmd_output('git', 'lfs', 'track', 'a.bin', 'b.bin')
        # First add the file we're going to move
        temp_git_dir.join('a.bin').write('a' * 10000)
        cmd_output('git', 'add', '--', '.')
        cmd_output('git', 'commit', '--no-gpg-sign', '-am', 'foo')
        # Now move it and make sure the hook still succeeds
        cmd_output('git', 'mv', 'a.bin', 'b.bin')
        assert main(('--maxkb', '9', 'b.bin')) == 0
