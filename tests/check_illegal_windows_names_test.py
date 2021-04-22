import sys

import pytest

from pre_commit_hooks.check_illegal_windows_names import (
    find_illegal_windows_names,
)
from pre_commit_hooks.check_illegal_windows_names import main
from pre_commit_hooks.check_illegal_windows_names import parents
from pre_commit_hooks.util import cmd_output

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
        assert find_illegal_windows_names(['f.py']) == 0


def test_adding_something(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_illegal_windows_names(['f.py']) == 0


@skip_win32  # pragma: win32 no cover
def test_adding_something_with_illegal_filename(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('CoM3.py').write("print('hello world')")
        cmd_output('git', 'add', 'CoM3.py')

        assert find_illegal_windows_names(['CoM3.py']) == 1


@skip_win32  # pragma: win32 no cover
def test_adding_files_with_illegal_directory(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.mkdir('lpt2').join('x').write('foo')
        cmd_output('git', 'add', '-A')

        assert find_illegal_windows_names([]) == 1


@skip_win32  # pragma: win32 no cover
def test_adding_files_with_illegal_deep_directories(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.mkdir('x').mkdir('y').join('pRn').write('foo')
        cmd_output('git', 'add', '-A')

        assert find_illegal_windows_names([]) == 1


@skip_win32  # pragma: win32 no cover
def test_integration(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert main(argv=[]) == 0

        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert main(argv=['f.py']) == 0

        temp_git_dir.join('CON.py').write("print('hello world')")
        cmd_output('git', 'add', 'CON.py')

        assert main(argv=['CON.py']) == 1
