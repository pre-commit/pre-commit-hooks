import os
import subprocess

import pytest

from pre_commit_hooks.destroyed_symlinks import find_destroyed_symlinks
from pre_commit_hooks.destroyed_symlinks import main
from testing.util import git_commit

TEST_SYMLINK = 'test_symlink'
TEST_SYMLINK_TARGET = '/doesnt/really/matters'
TEST_FILE = 'test_file'
TEST_FILE_RENAMED = f'{TEST_FILE}_renamed'


@pytest.fixture
def repo_with_destroyed_symlink(tmpdir):
    source_repo = tmpdir.join('src')
    os.makedirs(source_repo, exist_ok=True)
    test_repo = tmpdir.join('test')
    with source_repo.as_cwd():
        subprocess.check_call(('git', 'init'))
        os.symlink(TEST_SYMLINK_TARGET, TEST_SYMLINK)
        with open(TEST_FILE, 'w') as f:
            print('some random content', file=f)
        subprocess.check_call(('git', 'add', '.'))
        git_commit('-m', 'initial')
        assert b'120000 ' in subprocess.check_output(
            ('git', 'cat-file', '-p', 'HEAD^{tree}'),
        )
    subprocess.check_call(
        ('git', '-c', 'core.symlinks=false', 'clone', source_repo, test_repo),
    )
    with test_repo.as_cwd():
        subprocess.check_call(
            ('git', 'config', '--local', 'core.symlinks', 'true'),
        )
        subprocess.check_call(('git', 'mv', TEST_FILE, TEST_FILE_RENAMED))
    assert not os.path.islink(test_repo.join(TEST_SYMLINK))
    yield test_repo


def test_find_destroyed_symlinks(repo_with_destroyed_symlink):
    with repo_with_destroyed_symlink.as_cwd():
        assert find_destroyed_symlinks([]) == []
        assert main([]) == 0

        subprocess.check_call(('git', 'add', TEST_SYMLINK))
        assert find_destroyed_symlinks([TEST_SYMLINK]) == [TEST_SYMLINK]
        assert find_destroyed_symlinks([]) == []
        assert main([]) == 0
        assert find_destroyed_symlinks([TEST_FILE_RENAMED, TEST_FILE]) == []
        ALL_STAGED = [TEST_SYMLINK, TEST_FILE_RENAMED]
        assert find_destroyed_symlinks(ALL_STAGED) == [TEST_SYMLINK]
        assert main(ALL_STAGED) != 0

        with open(TEST_SYMLINK, 'a') as f:
            print(file=f)  # add trailing newline
        subprocess.check_call(['git', 'add', TEST_SYMLINK])
        assert find_destroyed_symlinks(ALL_STAGED) == [TEST_SYMLINK]
        assert main(ALL_STAGED) != 0

        with open(TEST_SYMLINK, 'w') as f:
            print('0' * len(TEST_SYMLINK_TARGET), file=f)
        subprocess.check_call(('git', 'add', TEST_SYMLINK))
        assert find_destroyed_symlinks(ALL_STAGED) == []
        assert main(ALL_STAGED) == 0

        with open(TEST_SYMLINK, 'w') as f:
            print('0' * (len(TEST_SYMLINK_TARGET) + 3), file=f)
        subprocess.check_call(('git', 'add', TEST_SYMLINK))
        assert find_destroyed_symlinks(ALL_STAGED) == []
        assert main(ALL_STAGED) == 0
