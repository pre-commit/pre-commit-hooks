
import pytest

from pre_commit_hooks.check_yaml import check_yaml
from testing.util import get_resource_path


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('bad_yaml.notyaml', 1),
    ('ok_yaml.yaml', 0),
))
def test_check_yaml(filename, expected_retval):
    ret = check_yaml([get_resource_path(filename)])
    assert ret == expected_retval
