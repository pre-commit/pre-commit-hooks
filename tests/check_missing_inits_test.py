import os

import pytest

from pre_commit_hooks.check_missing_inits import main


@pytest.fixture
def filepaths(tmpdir):
    dirs = ['a', 'b']
    files = ['a.py', 'b.py', '__init__.py']
    paths = []
    for d in dirs:
        directory = tmpdir / d
        os.mkdir(str(directory))
        for f in files:
            path = (directory / f)
            paths.append(str(path))
        # Nested directory
        if d == 'b':
            directory = directory / 'c'
            os.mkdir(str(directory))
            for f in files:
                path = (directory / f)
                paths.append(str(path))
    return paths


def test_has_inits(filepaths):
    for f in filepaths:
        with open(f, 'w'):
            pass

    assert main(argv=filepaths) == 0


def test_missing_inits(filepaths):
    remove = ''
    for f in filepaths:
        # Remove the init py file from the b directory
        if os.path.join('b', '__init__.py') in f:
            remove = str(f)
            continue
        with open(f, 'w'):
            pass
    filepaths.remove(remove)

    assert main(argv=filepaths) == 1


def test_nested_dirs_missing_inits(filepaths):
    remove = ''
    for f in filepaths:
        # Remove the init py file from a nested directory
        if os.path.join('b', 'c', '__init__.py') in f:
            remove = str(f)
            continue
        with open(f, 'w'):
            pass
    filepaths.remove(remove)

    assert main(argv=filepaths) == 1
