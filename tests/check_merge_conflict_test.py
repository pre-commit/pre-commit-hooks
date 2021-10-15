import os
import shutil

import pytest

from pre_commit_hooks.check_merge_conflict import main
from pre_commit_hooks.util import cmd_output
from testing.util import get_resource_path
from testing.util import git_commit


@pytest.fixture
def f1_is_a_conflict_file(tmpdir):
    # Make a merge conflict
    repo1 = tmpdir.join('repo1')
    repo1_f1 = repo1.join('f1')
    repo2 = tmpdir.join('repo2')
    repo2_f1 = repo2.join('f1')

    cmd_output('git', 'init', '--', str(repo1))
    with repo1.as_cwd():
        repo1_f1.ensure()
        cmd_output('git', 'add', '.')
        git_commit('-m', 'commit1')

    cmd_output('git', 'clone', str(repo1), str(repo2))

    # Commit in master
    with repo1.as_cwd():
        repo1_f1.write('parent\n')
        git_commit('-am', 'master commit2')

    # Commit in clone and pull
    with repo2.as_cwd():
        repo2_f1.write('child\n')
        git_commit('-am', 'clone commit2')
        cmd_output('git', 'pull', '--no-rebase', retcode=None)
        # We should end up in a merge conflict!
        f1 = repo2_f1.read()
        assert f1.startswith(
            '<<<<<<< HEAD\n'
            'child\n'
            '=======\n'
            'parent\n'
            '>>>>>>>',
        ) or f1.startswith(
            '<<<<<<< HEAD\n'
            'child\n'
            # diff3 conflict style git merges add this line:
            '||||||| merged common ancestors\n'
            '=======\n'
            'parent\n'
            '>>>>>>>',
        ) or f1.startswith(
            # .gitconfig with [pull] rebase = preserve causes a rebase which
            # flips parent / child
            '<<<<<<< HEAD\n'
            'parent\n'
            '=======\n'
            'child\n'
            '>>>>>>>',
        )
        assert os.path.exists(os.path.join('.git', 'MERGE_MSG'))
        yield repo2


@pytest.fixture
def repository_pending_merge(tmpdir):
    # Make a (non-conflicting) merge
    repo1 = tmpdir.join('repo1')
    repo1_f1 = repo1.join('f1')
    repo2 = tmpdir.join('repo2')
    repo2_f1 = repo2.join('f1')
    repo2_f2 = repo2.join('f2')
    cmd_output('git', 'init', str(repo1))
    with repo1.as_cwd():
        repo1_f1.ensure()
        cmd_output('git', 'add', '.')
        git_commit('-m', 'commit1')

    cmd_output('git', 'clone', str(repo1), str(repo2))

    # Commit in master
    with repo1.as_cwd():
        repo1_f1.write('parent\n')
        git_commit('-am', 'master commit2')

    # Commit in clone and pull without committing
    with repo2.as_cwd():
        repo2_f2.write('child\n')
        cmd_output('git', 'add', '.')
        git_commit('-m', 'clone commit2')
        cmd_output('git', 'pull', '--no-commit', '--no-rebase')
        # We should end up in a pending merge
        assert repo2_f1.read() == 'parent\n'
        assert repo2_f2.read() == 'child\n'
        assert os.path.exists(os.path.join('.git', 'MERGE_HEAD'))
        yield repo2


@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_merge_conflicts_git():
    assert main(['f1']) == 1


@pytest.mark.parametrize(
    'contents', (b'<<<<<<< HEAD\n', b'=======\n', b'>>>>>>> master\n'),
)
def test_merge_conflicts_failing(contents, repository_pending_merge):
    repository_pending_merge.join('f2').write_binary(contents)
    assert main(['f2']) == 1


@pytest.mark.parametrize(
    'contents', (b'# <<<<<<< HEAD\n', b'# =======\n', b'import mod', b''),
)
def test_merge_conflicts_ok(contents, f1_is_a_conflict_file):
    f1_is_a_conflict_file.join('f1').write_binary(contents)
    assert main(['f1']) == 0


@pytest.mark.usefixtures('f1_is_a_conflict_file')
def test_ignores_binary_files():
    shutil.copy(get_resource_path('img1.jpg'), 'f1')
    assert main(['f1']) == 0


def test_does_not_care_when_not_in_a_merge(tmpdir):
    f = tmpdir.join('README.md')
    f.write_binary(b'problem\n=======\n')
    assert main([str(f.realpath())]) == 0


def test_care_when_assumed_merge(tmpdir):
    f = tmpdir.join('README.md')
    f.write_binary(b'problem\n=======\n')
    assert main([str(f.realpath()), '--assume-in-merge']) == 1


def test_worktree_merge_conflicts(f1_is_a_conflict_file, tmpdir):
    worktree = tmpdir.join('worktree')
    cmd_output('git', 'worktree', 'add', str(worktree))
    with worktree.as_cwd():
        cmd_output(
            'git', 'pull', '--no-rebase', 'origin', 'master', retcode=None,
        )
        msg = f1_is_a_conflict_file.join('.git/worktrees/worktree/MERGE_MSG')
        assert msg.exists()
        test_merge_conflicts_git()
