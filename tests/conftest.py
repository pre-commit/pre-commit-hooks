from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.util import cmd_output
from testing.util import cwd


@pytest.yield_fixture
def in_tmpdir(tmpdir):
    with cwd(tmpdir.strpath):
        yield tmpdir


@pytest.yield_fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join('gits').strpath
    cmd_output('git', 'init', git_dir)
    yield git_dir
