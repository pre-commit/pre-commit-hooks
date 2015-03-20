from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.check_case_conflict import find_conflicting_filenames
from pre_commit_hooks.check_case_conflict import main
from pre_commit_hooks.util import cmd_output
from testing.util import cwd
from testing.util import write_file


def test_nothing_added(temp_git_dir):
    with cwd(temp_git_dir):
        assert find_conflicting_filenames(['f.py']) == 0


def test_adding_something(temp_git_dir):
    with cwd(temp_git_dir):
        write_file('f.py', "print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_conflicting_filenames(['f.py']) == 0


def test_adding_something_with_conflict(temp_git_dir):
    with cwd(temp_git_dir):
        write_file('f.py', "print('hello world')")
        cmd_output('git', 'add', 'f.py')
        write_file('F.py', "print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert find_conflicting_filenames(['f.py', 'F.py']) == 1


def test_added_file_not_in_pre_commits_list(temp_git_dir):
    with cwd(temp_git_dir):
        write_file('f.py', "print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_conflicting_filenames(['g.py']) == 0


def test_file_conflicts_with_committed_file(temp_git_dir):
    with cwd(temp_git_dir):
        write_file('f.py', "print('hello world')")
        cmd_output('git', 'add', 'f.py')
        cmd_output('git', 'commit', '--no-verify', '-m', 'Add f.py')

        write_file('F.py', "print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert find_conflicting_filenames(['F.py']) == 1


def test_integration(temp_git_dir):
    with cwd(temp_git_dir):
        assert main(argv=[]) == 0

        write_file('f.py', "print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert main(argv=['f.py']) == 0

        write_file('F.py', "print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert main(argv=['F.py']) == 1
