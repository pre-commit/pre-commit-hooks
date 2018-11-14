from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.detect_datetime_raw_manipulation import _check_file
from pre_commit_hooks.detect_datetime_raw_manipulation import main
from testing.util import get_resource_path


def test_flagged_file():
    rc = main([get_resource_path('detect_datetime_raw_manipulation/raw_timedelta_usage__flag.py')])
    assert rc == 1

    result = _check_file(get_resource_path('detect_datetime_raw_manipulation/raw_timedelta_usage__flag.py'))
    assert result == 10


def test_flagged_ignore():
    rc = main([get_resource_path('detect_datetime_raw_manipulation/raw_timedelta_usage__ignore.py')])
    assert rc == 0


def test_flagged_clean():
    rc = main([get_resource_path('detect_datetime_raw_manipulation/raw_timedelta_usage__clean.py')])
    assert rc == 0
