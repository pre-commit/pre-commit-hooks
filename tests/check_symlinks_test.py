import pytest

from pre_commit_hooks.check_symlinks import check_symlinks
from testing.util import get_resource_path


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('broken_symlink', 1),
    ('working_symlink', 0),
))
def test_check_symlinks(filename, expected_retval):
    ret = check_symlinks([get_resource_path(filename)])
    assert ret == expected_retval
