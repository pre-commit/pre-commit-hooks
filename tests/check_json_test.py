import pytest

from pre_commit_hooks.check_json import check_json
from testing.util import get_resource_path


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('bad_json.notjson', 1),
    ('ok_json.json', 0),
))
def test_check_json(filename, expected_retval):
    ret = check_json([get_resource_path(filename)])
    assert ret == expected_retval
