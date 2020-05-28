from pre_commit_hooks.check_path_edits import find_wrong_paths
from pre_commit_hooks.check_path_edits import main
from pre_commit_hooks.util import cmd_output


def test_nothing_added(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert find_wrong_paths(['f.py'], {'asd'}) == 0


def test_adding_something(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write("print('hello world')")
        cmd_output('git', 'add', 'f.py')

        assert find_wrong_paths(['f.py'], {'^f.*'}) == 1


def test_some_regex(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join('f.py').write('a' * 10000)

        # Should not fail when not added
        assert find_wrong_paths(['f.py'], {'.*'}) == 0

        cmd_output('git', 'add', 'f.py')

        assert find_wrong_paths(['f.py'], {'.*'}) == 1

        assert find_wrong_paths(['f.py'], {'dasd', 'py', 'asd'}) == 1

        assert find_wrong_paths(['f.py'], {'^py'}) == 0


def test_integration(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert main(argv=[]) == 0

        temp_git_dir.join('f.py').write('a')
        cmd_output('git', 'add', 'f.py')

        # Should not fail with default
        assert main(argv=['f.py']) == 0

        assert main(argv=['--pattern', 'f.py', 'f.py']) == 1
