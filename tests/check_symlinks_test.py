import os

import pytest

from pre_commit_hooks.check_symlinks import main


xfail_symlink = pytest.mark.xfail(os.name == 'nt', reason='No symlink support')


@xfail_symlink
@pytest.mark.parametrize(
    ('dest', 'expected'), (('exists', 0), ('does-not-exist', 1)),
)
def test_main(tmpdir, dest, expected):  # pragma: no cover (symlinks)
    tmpdir.join('exists').ensure()
    symlink = tmpdir.join('symlink')
    symlink.mksymlinkto(tmpdir.join(dest))
    assert main((str(symlink),)) == expected


def test_main_normal_file(tmpdir):
    assert main((str(tmpdir.join('f').ensure()),)) == 0
