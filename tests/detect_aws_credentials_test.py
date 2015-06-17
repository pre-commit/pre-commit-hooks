import pytest

from pre_commit_hooks.detect_aws_credentials import main
from testing.util import get_resource_path


# Input filename, expected return value
TESTS = (
    ('with_no_secrets.txt', 0),
    ('with_secrets.txt', 1),
    ('nonsense.txt', 0),
    ('ok_json.json', 0),
)

NO_CREDENTIALS_TEST = (
    ('with_secrets.txt', 2),
)


@pytest.mark.parametrize(('filename', 'expected_retval'), TESTS)
def test_detect_aws_credentials(filename, expected_retval):
    # with a valid credentials file
    ret = main(
        [get_resource_path(filename), "--credentials-file=testing/resources/sample_aws_credentials"]
    )
    assert ret == expected_retval


@pytest.mark.parametrize(('filename', 'expected_retval'), NO_CREDENTIALS_TEST)
def test_non_existent_credentials(filename, expected_retval):
    # with a non-existent credentials file
    ret = main(
        [get_resource_path(filename), "--credentials-file=testing/resources/credentailsfilethatdoesntexist"]
    )
    assert ret == expected_retval
