from __future__ import absolute_import
from __future__ import unicode_literals

import os
import shutil

import pytest

from pre_commit_hooks.check_merge_conflict import detect_merge_conflict
from pre_commit_hooks.util import cmd_output
from testing.util import get_resource_path
from testing.util import write_file


# pylint:disable=unused-argument


@pytest.yield_fixture
def f1_is_a_conflict_file(tmpdir):
    # Make a merge conflict
    repo1 = tmpdir.join('repo1')
    repo1_f1 = repo1.join('f1')
    repo2 = tmpdir.join('repo2')
    repo2_f1 = repo2.join('f1')

    cmd_output('git', 'init', '--', repo1.strpath)
    with repo1.as_cwd():
        repo1_f1.ensure()
        cmd_output('git', 'add', '--', repo1_f1.strpath)
        cmd_output('git', 'commit', '--no-gpg-sign', '-m', 'commit1')

    cmd_output('git', 'clone', repo1.strpath, repo2.strpath)

    # Commit in master
    with repo1.as_cwd():
        repo1_f1.write('parent\n')
        cmd_output('git', 'commit', '--no-gpg-sign', '-am', 'master commit2')

    # Commit in clone and pull
    with repo2.as_cwd():
        repo2_f1.write('child\n')
        cmd_output('git', 'commit', '--no-gpg-sign', '-am', 'clone commit2')
        cmd_output('git', 'pull', retcode=None)
        # We should end up in a merge conflict!
        f1 = repo2_f1.read()
        assert f1.startswith(
            '<<<<<<< HEAD\n'
            'child\n'
            '=======\n'
            'parent\n'
            '>>>>>>>'
        ) or f1.startswith(
            '<<<<<<< HEAD\n'
            'child\n'
            # diff3 conflict style git merges add this line:
            '||||||| merged common ancestors\n'
            '=======\n'
            'parent\n'
            '>>>>>>>'
        )
        assert os.path.exists(os.path.join('.git', 'MERGE_MSG'))
        yield


@pytest.yield_fixture
def repository_is_pending_merge(tmpdir):
    # Make a (non-conflicting) merge
    repo1 = tmpdir.join('repo1')
    repo1_f1 = repo1.join('f1')
    repo2 = tmpdir.join('repo2')
    repo2_f1 = repo2.join('f1')
    repo2_f2 = repo2.join('f2')
    cmd_output('git', 'init', repo1.strpath)
    with repo1.as_cwd():
        repo1_f1.ensure()
        cmd_output('git', 'add', '--', repo1_f1.strpath)
        cmd_output('git', 'commit', '--no-gpg-sign', '-m', 'commit1')

    cmd_output('git', 'clone', repo1.strpath, repo2.strpath)

    # Commit in master
    with repo1.as_cwd():
        repo1_f1.write('parent\n')
        cmd_output('git', 'commit', '--no-gpg-sign', '-am', 'master commit2')

    # Commit in clone and pull without committing
    with repo2.as_cwd():
        repo2_f2.write('child\n')
        cmd_output('git', 'add', '--', repo2_f2.strpath)
        cmd_output('git', 'commit', '--no-gpg-sign', '-m', 'clone commit2')
        cmd_output('git', 'pull', '--no-commit')
        # We should end up in a pending merge
        assert repo2_f1.read() == 'parent\n'
        assert repo2_f2.read() == 'child\n'
        assert os.path.exists(os.path.join('.git', 'MERGE_HEAD'))
        yield


@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_merge_conflicts_git():
    assert detect_merge_conflict(['f1']) == 1


@pytest.mark.parametrize(
    'failing_contents', ('<<<<<<< HEAD\n', '=======\n', '>>>>>>> master\n'),
)
@pytest.mark.usefixtures('repository_is_pending_merge')
def test_merge_conflicts_failing(failing_contents):
    write_file('f2', failing_contents)
    assert detect_merge_conflict(['f2']) == 1


@pytest.mark.parametrize(
    'ok_contents', ('# <<<<<<< HEAD\n', '# =======\n', 'import my_module', ''),
)
@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_merge_conflicts_ok(ok_contents):
    write_file('f1', ok_contents)
    assert detect_merge_conflict(['f1']) == 0


@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_ignores_binary_files():
    shutil.copy(get_resource_path('img1.jpg'), 'f1')
    assert detect_merge_conflict(['f1']) == 0


def test_does_not_care_when_not_in_a_merge(tmpdir):
    tmpdir.join('README.md').write('problem\n=======\n')
    assert detect_merge_conflict(['README.md']) == 0
