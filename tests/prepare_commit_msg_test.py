from __future__ import annotations

import pytest

from pre_commit_hooks.prepare_commit_msg import get_current_branch
from pre_commit_hooks.prepare_commit_msg import main
from pre_commit_hooks.prepare_commit_msg import update_commit_file
from pre_commit_hooks.util import cmd_output
from pre_commit_hooks.util import get_template_path


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
        b'',
        'test',  # this should not trigger anything
        'prepare_commit_msg_prepend.j2',
    ),
    (
        b'',
        b'',
        'master',  # this should not trigger anything
        'prepare_commit_msg_prepend.j2',
    ),
    (
        b'',
        b'[1.0.0] ',
        'release/1.0.0',  # but this should
        get_template_path('prepare_commit_msg_prepend.j2'),
    ),
    (
        b'',
        b'[TT-01] ',
        'feature/TT-01',
        get_template_path('prepare_commit_msg_prepend.j2'),
    ),
    (
        b'[TT-02] Some message',
        b'[TT-02] Some message',
        'feature/TT-02',
        get_template_path('prepare_commit_msg_prepend.j2'),
    ),
    (
        b'Initial message',
        b'[TT-03] Initial message',
        'feature/TT-03',
        get_template_path('prepare_commit_msg_prepend.j2'),
    ),
    (
        b'',
        b'\n\nRelates: #AA-01\n\n',
        'feature/AA-01',
        get_template_path('prepare_commit_msg_append.j2'),
    ),
    (
        b'Initial message',
        b'Initial message\n\nRelates: #AA-02\n\n',
        'feature/AA-02',
        get_template_path('prepare_commit_msg_append.j2'),
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
        parts = branch_name.split('/')
        ticket = str(parts[1]) if len(parts) > 1 else str(parts[0])
        update_commit_file(path, template, ticket)

        # here the filtering is still not in place
        if branch_name == 'test':
            expected_val = b''

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
                '-p', '(?<=release/).*',
                str(path),
            ],
        ) == 0
        assert path.read_binary() == expected_val


TESTS_TEMPLATES = (
    (
        b'Initial Message\n\n# Git commented\n# output simulated',
        b'[1.0.0] Initial Message\n\n# Git commented\n# output simulated',
        'release/1.0.0',  # but this should
        get_template_path('prepare_commit_msg_prepend.j2'),
    ),
    (
        b'Initial Message\n# Git commented\n# output simulated',
        b'Initial Message\n\nRelates: #1.0.0\n\n'
        b'# Git commented\n# output simulated',
        'release/1.0.0',  # but this should
        get_template_path('prepare_commit_msg_append.j2'),
    ),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_val', 'branch_name', 'template'),
    TESTS_TEMPLATES,
)
def test_main_separating_content(
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
                '-p', '(?<=release/).*',
                str(path),
            ],
        ) == 0
        assert path.read_binary() == expected_val
