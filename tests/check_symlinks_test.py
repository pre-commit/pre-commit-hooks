import os

import pytest

from pre_commit_hooks.check_symlinks import check_symlinks


xfail_symlink = pytest.mark.xfail(os.name == 'nt', reason='No symlink support')


@xfail_symlink
@pytest.mark.parametrize(
    ('dest', 'expected'), (('exists', 0), ('does-not-exist', 1)),
)
def test_check_symlinks(tmpdir, dest, expected):  # pragma: no cover (symlinks)
    tmpdir.join('exists').ensure()
    symlink = tmpdir.join('symlink')
    symlink.mksymlinkto(tmpdir.join(dest))
    assert check_symlinks((symlink.strpath,)) == expected


def test_check_symlinks_normal_file(tmpdir):
    assert check_symlinks((tmpdir.join('f').ensure().strpath,)) == 0
