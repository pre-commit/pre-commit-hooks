from __future__ import annotations

import pytest

from pre_commit_hooks.prepare_commit_msg import get_current_branch
from pre_commit_hooks.prepare_commit_msg import get_jinja_env
from pre_commit_hooks.prepare_commit_msg import main
from pre_commit_hooks.prepare_commit_msg import update_commit_file
from pre_commit_hooks.util import cmd_output


def test_current_branch(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'feature')
        assert get_current_branch() == 'feature'

        cmd_output('git', 'checkout', '-b', 'feature/branch')
        assert get_current_branch() == 'feature/branch'


# Input, expected value, branch, template
TESTS = (
    (
        b'',
        b'[TT-01] ',
        'feature/TT-01',
        'prepare_commit_msg_prepend.j2',
    ),
    (
        b'[TT-02] Some message',
        b'[TT-02] Some message',
        'feature/TT-02',
        'prepare_commit_msg_prepend.j2',
    ),
    (
        b'Initial message',
        b'[TT-03] Initial message',
        'feature/TT-03',
        'prepare_commit_msg_prepend.j2',
    ),
    (
        b'',
        b'\n\nRelates: AA-01',
        'feature/AA-01',
        'prepare_commit_msg_append.j2',
    ),
    (
        b'Initial message',
        b'Initial message\n\nRelates: AA-02',
        'feature/AA-02',
        'prepare_commit_msg_append.j2',
    ),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_val', 'branch_name', 'template'),
    TESTS,
)
def test_update_commit_file(
        input_s, expected_val, branch_name, template,
        temp_git_dir,
):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join('COMMIT_EDITMSG')
        path.write_binary(input_s)
        ticket = branch_name.split('/')[1]
        jinja = get_jinja_env()
        update_commit_file(jinja, path, template, ticket)

        assert path.read_binary() == expected_val


@pytest.mark.parametrize(
    ('input_s', 'expected_val', 'branch_name', 'template'),
    TESTS,
)
def test_main(
        input_s, expected_val, branch_name, template,
        temp_git_dir,
):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join('file.txt')
        path.write_binary(input_s)
        assert path.read_binary() == input_s

        cmd_output('git', 'checkout', '-b', branch_name)
        assert main(
            argv=[
                '-t', template,
                '-p', '(?<=feature/).*',
                str(path),
            ],
        ) == 0
        assert path.read_binary() == expected_val
