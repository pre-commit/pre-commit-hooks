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


@pytest.mark.parametrize(('filename', 'expected_retval'), TESTS)
def test_detect_aws_credentials(filename, expected_retval):
    # with a valid credentials file
    ret = main(
        [get_resource_path(filename), "--credentials-file=testing/resources/sample_aws_credentials"]
    )
    assert ret == expected_retval


def test_non_existent_credentials(capsys):
    # with a non-existent credentials file
    ret = main((
        get_resource_path('with_secrets.txt'),
        "--credentials-file=testing/resources/credentailsfilethatdoesntexist"
    ))
    assert ret == 2
    out, _ = capsys.readouterr()
    assert out == (
        'No aws keys were configured at '
        'testing/resources/credentailsfilethatdoesntexist\n'
        'Configure them with --credentials-file\n'
    )
