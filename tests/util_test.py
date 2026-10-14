from __future__ import annotations

import sys

import pytest

from pre_commit_hooks.util import added_files
from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output
from pre_commit_hooks.util import zsplit


def test_raises_on_error():
    with pytest.raises(CalledProcessError):
        cmd_output('sh', '-c', 'exit 1')


def test_output():
    ret = cmd_output('sh', '-c', 'echo hi')
    assert ret == 'hi\n'


skip_windows_filename = pytest.mark.skipif(
    sys.platform == 'win32', reason='invalid Windows filename',
)


@pytest.mark.parametrize(
    'filename', (
        'mañana.txt',
        pytest.param('line\nbreak.txt', marks=skip_windows_filename),
        pytest.param('tab\tfile.txt', marks=skip_windows_filename),
    ),
)
def test_added_files_preserves_quoted_names(temp_git_dir, filename):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', 'core.quotePath', 'true')
        temp_git_dir.join(filename).write('content')
        cmd_output('git', 'add', '--', filename)
        assert added_files() == {filename}


@pytest.mark.parametrize('out', ('\0f1\0f2\0', '\0f1\0f2', 'f1\0f2\0'))
def test_check_zsplits_str_correctly(out):
    assert zsplit(out) == ['f1', 'f2']


@pytest.mark.parametrize('out', ('\0\0', '\0', ''))
def test_check_zsplit_returns_empty(out):
    assert zsplit(out) == []
