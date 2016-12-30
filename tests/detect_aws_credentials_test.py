import pytest

from pre_commit_hooks.detect_aws_credentials import get_aws_credential_files_from_env
from pre_commit_hooks.detect_aws_credentials import get_aws_secrets_from_env
from pre_commit_hooks.detect_aws_credentials import get_aws_secrets_from_file
from pre_commit_hooks.detect_aws_credentials import main
from testing.util import get_resource_path


def test_get_aws_credentials_file_from_env(monkeypatch):
    """Test that reading credential files names from environment variables works."""
    monkeypatch.delenv('AWS_CREDENTIAL_FILE', raising=False)
    monkeypatch.delenv('AWS_SHARED_CREDENTIALS_FILE', raising=False)
    monkeypatch.delenv('BOTO_CONFIG', raising=False)
    assert get_aws_credential_files_from_env() == set()
    monkeypatch.setenv('AWS_CREDENTIAL_FILE', '/foo')
    assert get_aws_credential_files_from_env() == {'/foo'}
    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE', '/bar')
    assert get_aws_credential_files_from_env() == {'/foo', '/bar'}
    monkeypatch.setenv('BOTO_CONFIG', '/baz')
    assert get_aws_credential_files_from_env() == {'/foo', '/bar', '/baz'}
    monkeypatch.setenv('AWS_CONFIG_FILE', '/xxx')
    assert get_aws_credential_files_from_env() == {'/foo', '/bar', '/baz', '/xxx'}
    monkeypatch.setenv('AWS_DUMMY_KEY', 'foobar')
    assert get_aws_credential_files_from_env() == {'/foo', '/bar', '/baz', '/xxx'}


def test_get_aws_secrets_from_env(monkeypatch):
    """Test that reading secrets from environment variables works."""
    monkeypatch.delenv('AWS_SECRET_ACCESS_KEY', raising=False)
    monkeypatch.delenv('AWS_SESSION_TOKEN', raising=False)
    assert get_aws_secrets_from_env() == set()
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'foo')
    assert get_aws_secrets_from_env() == {'foo'}
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'bar')
    assert get_aws_secrets_from_env() == {'foo', 'bar'}
    monkeypatch.setenv('AWS_SECURITY_TOKEN', 'baz')
    assert get_aws_secrets_from_env() == {'foo', 'bar', 'baz'}
    monkeypatch.setenv('AWS_DUMMY_KEY', 'baz')
    assert get_aws_secrets_from_env() == {'foo', 'bar', 'baz'}


@pytest.mark.parametrize(('filename', 'expected_keys'), (
    ('aws_config_with_secret.ini', {
        'z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb'}),
    ('aws_config_with_session_token.ini', {'foo'}),
    ('aws_config_with_secret_and_session_token.ini',
     {'z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb', 'foo'}),
    ('aws_config_with_multiple_sections.ini', {
        '7xebzorgm5143ouge9gvepxb2z70bsb2rtrh099e',
        'z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb',
        'ixswosj8gz3wuik405jl9k3vdajsnxfhnpui38ez',
        'foo'}),
    ('aws_config_without_secrets.ini', set()),
    ('nonsense.txt', set()),
    ('ok_json.json', set()),
))
def test_get_aws_secrets_from_file(filename, expected_keys):
    """Test that reading secrets from files works."""
    keys = get_aws_secrets_from_file(get_resource_path(filename))
    assert keys == expected_keys


# Input filename, expected return value
TESTS = (
    ('aws_config_with_secret.ini', 1),
    ('aws_config_with_session_token.ini', 1),
    ('aws_config_with_multiple_sections.ini', 1),
    ('aws_config_without_secrets.ini', 0),
    ('nonsense.txt', 0),
    ('ok_json.json', 0),
)


@pytest.mark.parametrize(('filename', 'expected_retval'), TESTS)
def test_detect_aws_credentials(filename, expected_retval):
    """Test if getting configured AWS secrets from files to be checked in works."""

    # with a valid credentials file
    ret = main((
        get_resource_path(filename),
        "--credentials-file=testing/resources/aws_config_with_multiple_sections.ini",
    ))
    assert ret == expected_retval


def test_non_existent_credentials(capsys, monkeypatch):
    """Test behavior with no configured AWS secrets."""
    monkeypatch.setattr(
        'pre_commit_hooks.detect_aws_credentials.get_aws_secrets_from_env',
        lambda: set())
    monkeypatch.setattr(
        'pre_commit_hooks.detect_aws_credentials.get_aws_secrets_from_file',
        lambda x: set())
    ret = main((
        get_resource_path('aws_config_without_secrets.ini'),
        "--credentials-file=testing/resources/credentailsfilethatdoesntexist"
    ))
    assert ret == 2
    out, _ = capsys.readouterr()
    assert out == ('No AWS keys were found in the configured credential files '
                   'and environment variables.\nPlease ensure you have the '
                   'correct setting for --credentials-file\n')
