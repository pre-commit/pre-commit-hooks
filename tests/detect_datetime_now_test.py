import pytest

from pre_commit_hooks.detect_datetime_now import main

TESTS = (
    ('from datetime import datetime\ncurrent_date = datetime.now()', 1),
    ('from datetime import datetime', 0),
)


@pytest.mark.parametrize(('input_s', 'expected_return_value'), TESTS)
def test_datetime_now_usage(input_s, expected_return_value, tmpdir):
    """Test behavior with no datetime.now being used on code."""
    path = tmpdir.join('test_script.py')
    path.write(input_s)
    using_datetime = main([path.strpath])
    assert using_datetime == expected_return_value
