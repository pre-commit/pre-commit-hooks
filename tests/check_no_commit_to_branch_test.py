from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.no_commit_to_branch import is_on_branch
from pre_commit_hooks.no_commit_to_branch import main
from pre_commit_hooks.util import cmd_output


def test_other_branch(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'anotherbranch')
        assert is_on_branch(('master', )) is False


def test_multi_branch(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'another/branch')
        assert is_on_branch(('master', )) is False


def test_multi_branch_fail(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'another/branch')
        assert is_on_branch(('another/branch', )) is True


def test_master_branch(temp_git_dir):
    with temp_git_dir.as_cwd():
        assert is_on_branch(('master', )) is True


def test_main_b_call(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'other')
        assert main(['-b', 'other']) == 1


def test_main_branch_call(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'other')
        assert main(['--branch', 'other']) == 1


def test_main_default_call(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'anotherbranch')
        assert main() == 0
