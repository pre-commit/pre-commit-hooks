import pytest

from pre_commit_hooks.util import cmd_output


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join('gits')
    cmd_output('git', 'init', '--', git_dir.strpath)
    yield git_dir
