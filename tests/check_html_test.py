from __future__ import annotations

import pytest

from pre_commit_hooks.check_html import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('bad_html_not_closed.html', 1),
        ('bad_html_too_many_close.html', 1),
        ('bad_html_wrong_close.html', 1),
        ('ok_html_fragment.html', 0),
        ('ok_html_page.html', 0),
    ),
)
def test_main(filename, expected_retval):
    ret = main([get_resource_path(filename)])
    assert ret == expected_retval
