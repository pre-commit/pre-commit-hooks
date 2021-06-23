import sys

import pytest

from pre_commit_hooks.check_case_conflict import find_conflicting_filenames
from pre_commit_hooks.check_case_conflict import main
from pre_commit_hooks.check_case_conflict import parents
from pre_commit_hooks.util import cmd_output
from testing.util import git_commit

skip_win32 = pytest.mark.skipif(
    sys.platform == 'win32',
    reason='case conflicts between directories and files',
)


def test_parents():
    assert set(parents('a')) == set()
    assert set(parents('a/b')) == {'a'}
    assert set(parents('a/b/c')) == {'a/b', 'a'}
    assert set(parents('a/b/c/d')) == {'a/b/c', 'a/b', 'a'}


def test_nothing_added(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert find_conflicting_filenames(['f.py']) == 0


def test_adding_something(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_conflicting_filenames(['f.py']) == 0


def test_adding_something_with_conflict(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')
        temp_git_dir.join('F.py').write("print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert find_conflicting_filenames(['f.py', 'F.py']) == 1


@skip_win32  # pragma: win32 no cover
def test_adding_files_with_conflicting_directories(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.mkdir('dir').join('x').write('foo')
        temp_git_dir.mkdir('DIR').join('y').write('foo')
        cmd_output('git', 'add', '-A')

        assert find_conflicting_filenames([]) == 1


@skip_win32  # pragma: win32 no cover
def test_adding_files_with_conflicting_deep_directories(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.mkdir('x').mkdir('y').join('z').write('foo')
        temp_git_dir.join('X').write('foo')
        cmd_output('git', 'add', '-A')

        assert find_conflicting_filenames([]) == 1


@skip_win32  # pragma: win32 no cover
def test_adding_file_with_conflicting_directory(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.mkdir('dir').join('x').write('foo')
        temp_git_dir.join('DIR').write('foo')
        cmd_output('git', 'add', '-A')

        assert find_conflicting_filenames([]) == 1


def test_added_file_not_in_pre_commits_list(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_conflicting_filenames(['g.py']) == 0


def test_file_conflicts_with_committed_file(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')
        git_commit('-m', 'Add f.py')

        temp_git_dir.join('F.py').write("print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert find_conflicting_filenames(['F.py']) == 1


@skip_win32  # pragma: win32 no cover
def test_file_conflicts_with_committed_dir(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.mkdir('dir').join('x').write('foo')
        cmd_output('git', 'add', '-A')
        git_commit('-m', 'Add f.py')

        temp_git_dir.join('DIR').write('foo')
        cmd_output('git', 'add', '-A')

        assert find_conflicting_filenames([]) == 1


def test_integration(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert main(argv=[]) == 0

        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert main(argv=['f.py']) == 0

        temp_git_dir.join('F.py').write("print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert main(argv=['F.py']) == 1
