from __future__ import absolute_import
from __future__ import unicode_literals

from plumbum import local

from pre_commit_hooks.check_added_large_files import find_large_added_files
from pre_commit_hooks.check_added_large_files import main
from testing.util import write_file


def test_nothing_added(temp_git_dir):
    with local.cwd(temp_git_dir):
        assert find_large_added_files(['f.py'], 0) == 0


def test_adding_something(temp_git_dir):
    with local.cwd(temp_git_dir):
        write_file('f.py', "print('hello world')")
        local['git']('add', 'f.py')

        # Should fail with max size of 0
        assert find_large_added_files(['f.py'], 0) == 1


def test_add_something_giant(temp_git_dir):
    with local.cwd(temp_git_dir):
        write_file('f.py', 'a' * 10000)

        # Should not fail when not added
        assert find_large_added_files(['f.py'], 0) == 0

        local['git']('add', 'f.py')

        # Should fail with strict bound
        assert find_large_added_files(['f.py'], 0) == 1

        # Should also fail with actual bound
        assert find_large_added_files(['f.py'], 9) == 1

        # Should pass with higher bound
        assert find_large_added_files(['f.py'], 10) == 0


def test_added_file_not_in_pre_commits_list(temp_git_dir):
    with local.cwd(temp_git_dir):
        write_file('f.py', "print('hello world')")
        local['git']('add', 'f.py')

        # Should pass even with a size of 0
        assert find_large_added_files(['g.py'], 0) == 0


def test_integration(temp_git_dir):
    with local.cwd(temp_git_dir):
        assert main(argv=[]) == 0

        write_file('f.py', 'a' * 10000)
        local['git']('add', 'f.py')

        # Should not fail with default
        assert main(argv=['f.py']) == 0

        # Should fail with --maxkb
        assert main(argv=['--maxkb', '9', 'f.py']) == 1
