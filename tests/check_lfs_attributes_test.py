from __future__ import annotations

import shutil

import pytest

from pre_commit_hooks.check_lfs_attributes import check_lfs_attributes
from pre_commit_hooks.check_lfs_attributes import main
from pre_commit_hooks.check_lfs_attributes import select_lfs_attr_files
from pre_commit_hooks.check_lfs_attributes import select_lfs_tree_files
from pre_commit_hooks.util import cmd_output
from testing.util import git_commit


@pytest.fixture
def temp_git_dir_as_cwd(temp_git_dir):
    with temp_git_dir.as_cwd():
        yield temp_git_dir


def has_gitlfs():
    return shutil.which('git-lfs') is not None


xfailif_no_gitlfs = pytest.mark.xfail(
    not has_gitlfs(), reason='This test requires git-lfs',
)


@xfailif_no_gitlfs
def test_select_lfs_attr_files(temp_git_dir_as_cwd):  # pragma: no cover
    cmd_output('git', 'lfs', 'install', '--local')
    cmd_output('git', 'lfs', 'track', '*.bin')
    assert select_lfs_attr_files(set()) == set()
    assert select_lfs_attr_files({'b.txt'}) == set()
    assert select_lfs_attr_files({'a.bin', 'b.txt'}) == {'a.bin'}


@xfailif_no_gitlfs
def test_select_lfs_tree_files(temp_git_dir_as_cwd):  # pragma: no cover
    cmd_output('git', 'lfs', 'install', '--local')
    cmd_output('git', 'lfs', 'track', '*.bin')
    temp_git_dir_as_cwd.join('a.bin').write('a')
    temp_git_dir_as_cwd.join('b.bin').write('b')
    cmd_output('git', 'add', 'a.bin')
    assert select_lfs_tree_files(set()) == set()
    assert select_lfs_tree_files({'b.bin'}) == set()
    assert select_lfs_tree_files({'a.bin', 'b.bin'}) == {'a.bin'}


@xfailif_no_gitlfs
def test_nothing_added(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert check_lfs_attributes(['a.bin']) == 0


@xfailif_no_gitlfs
def test_add_as_lfs_object(temp_git_dir_as_cwd):  # pragma: no cover
    temp_git_dir_as_cwd.join('a.bin').write('a')
    cmd_output('git', 'lfs', 'install', '--local')
    cmd_output('git', 'lfs', 'track', '*.bin')
    cmd_output('git', 'add', 'a.bin')
    assert main(('a.bin',)) == 0


@xfailif_no_gitlfs
def test_regular_object_but_tracked_by_lfs(temp_git_dir_as_cwd, capsys):  # pragma: no cover
    temp_git_dir_as_cwd.join('a.bin').write('a')
    cmd_output('git', 'lfs', 'install', '--local')
    cmd_output('git', 'add', 'a.bin')
    cmd_output('git', 'lfs', 'track', '*.bin')
    assert main(('a.bin',)) == 1
    out, _ = capsys.readouterr()
    assert 'a.bin is tracked by LFS but added as a regular object' in out


@xfailif_no_gitlfs
def test_lfs_object_but_not_tracked(temp_git_dir_as_cwd, capsys):  # pragma: no cover
    temp_git_dir_as_cwd.join('a.bin').write('a')
    cmd_output('git', 'lfs', 'install', '--local')
    cmd_output('git', 'lfs', 'track', '*.bin')
    cmd_output('git', 'add', 'a.bin')
    cmd_output('git', 'lfs', 'untrack', '*.bin')
    assert main(('a.bin',)) == 1
    out, _ = capsys.readouterr()
    assert 'a.bin is added as LFS object but not tracked' in out
