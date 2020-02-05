from pre_commit_hooks.check_case_conflict import find_conflicting_filenames
from pre_commit_hooks.check_case_conflict import main
from pre_commit_hooks.util import cmd_output


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


def test_added_file_not_in_pre_commits_list(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_conflicting_filenames(['g.py']) == 0


def test_file_conflicts_with_committed_file(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')
        cmd_output('git', 'commit', '--no-gpg-sign', '-n', '-m', 'Add f.py')

        temp_git_dir.join('F.py').write("print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert find_conflicting_filenames(['F.py']) == 1


def test_integration(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert main(argv=[]) == 0

        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert main(argv=['f.py']) == 0

        temp_git_dir.join('F.py').write("print('hello world')")
        cmd_output('git', 'add', 'F.py')

        assert main(argv=['F.py']) == 1
