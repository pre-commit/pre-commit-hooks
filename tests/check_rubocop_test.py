import pytest

from pre_commit_hooks.check_rubocop import check_rubocop
from testing.util import get_resource_path


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('invalid_ruby.rb', 1),
    ('valid_ruby.rb', 0),
))
def test_check_rubocop(filename, expected_retval):
    ret = check_rubocop([get_resource_path(filename)])
    assert ret == expected_retval
