from __future__ import absolute_import
from __future__ import unicode_literals

import io

import pytest

from pre_commit_hooks.check_merge_conflict import detect_merge_conflict
from pre_commit_hooks.util import cmd_output
from testing.util import cwd
from testing.util import write_file


# pylint:disable=unused-argument


@pytest.yield_fixture
def f1_is_a_conflict_file(in_tmpdir):
    # Make a merge conflict
    cmd_output('git', 'init', 'repo1')
    with cwd('repo1'):
        io.open('f1', 'w').close()
        cmd_output('git', 'add', 'f1')
        cmd_output('git', 'commit', '-m' 'commit1')

    cmd_output('git', 'clone', 'repo1', 'repo2')

    # Commit in master
    with cwd('repo1'):
        write_file('f1', 'parent\n')
        cmd_output('git', 'commit', '-am', 'master commit2')

    # Commit in clone and pull
    with cwd('repo2'):
        write_file('f1', 'child\n')
        cmd_output('git', 'commit', '-am', 'clone commit2')
        cmd_output('git', 'pull', retcode=None)
        # We should end up in a merge conflict!
        assert io.open('f1').read().startswith(
            '<<<<<<< HEAD\n'
            'child\n'
            '=======\n'
            'parent\n'
            '>>>>>>>'
        )
        yield


@pytest.mark.parametrize(
    'failing_contents', ('<<<<<<< HEAD', '=======', '>>>>>>> master'),
)
@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_merge_conflicts_failing(failing_contents):
    write_file('f1', failing_contents)
    assert detect_merge_conflict(['f1']) == 1


@pytest.mark.parametrize(
    'ok_contents', ('# <<<<<<< HEAD', '# =======', 'import my_module', ''),
)
@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_merge_conflicts_ok(ok_contents):
    write_file('f1', ok_contents)
    assert detect_merge_conflict(['f1']) == 0


@pytest.mark.usefixtures('in_tmpdir')
def test_does_not_care_when_not_in_a_conflict():
    with io.open('README.md', 'w') as readme_file:
        readme_file.write('pre-commit\n=================\n')
    assert detect_merge_conflict(['README.md']) == 0
