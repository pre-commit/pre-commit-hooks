from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from plumbum import local


@pytest.yield_fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join('gits').strpath
    local['git']('init', git_dir)
    yield git_dir
