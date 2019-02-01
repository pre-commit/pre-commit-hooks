import pytest

from pre_commit_hooks.check_xml import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('bad_xml.notxml', 1),
        ('ok_xml.xml', 0),
    ),
)
def test_main(filename, expected_retval):
    ret = main([get_resource_path(filename)])
    assert ret == expected_retval
