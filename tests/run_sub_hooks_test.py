import re

import pytest

from pre_commit_hooks.run_sub_hooks import main


@pytest.fixture
def temp_sub_dir(temp_git_dir):
    """Temporary git subdirectory with pre-commit config inside of it"""
    with temp_git_dir.as_cwd():
        sub_dir = temp_git_dir.mkdir('subdir')
        sub_dir.join('.pre-commit-config.yaml').write(
            """\
repos:
        -   repo: https://github.com/pre-commit/pre-commit-hooks
            rev: v2.0.0
            hooks:
            -   id: trailing-whitespace\
"""
        )
        yield sub_dir


INFO_PATTERN = re.compile(r'^\s*(\[INFO\] [^\n]+\n)+', flags=re.M)


def test_clean_run(temp_sub_dir, capfd):
    assert main(['--target', str(temp_sub_dir), '--all-files']) == 0
    captured = capfd.readouterr()
    assert (  # noqa: E501
        INFO_PATTERN.sub('', captured.out) ==
        """\
Trim Trailing Whitespace.................................................Passed
"""
    )
    assert captured.err == ''


def test_only_sub_dir_files_when_all_files(temp_git_dir, temp_sub_dir, capfd):
    temp_git_dir.join('file1.yaml').write('some trailing whitespace ->    ')
    temp_sub_dir.join('file2.yaml').write('some trailing whitespace ->    ')
    assert main(['--target', str(temp_sub_dir), '--all-files']) == 1
    captured = capfd.readouterr()
    assert (  # noqa: E501
        INFO_PATTERN.sub('', captured.out) ==
        """\
Trim Trailing Whitespace.................................................Failed
hookid: trailing-whitespace

Fixing subdir/file2.yaml

"""
    )
    assert captured.err == ''
