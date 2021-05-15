from unittest.mock import patch

import pytest

from pre_commit_hooks.detect_aws_credentials import get_aws_cred_files_from_env
from pre_commit_hooks.detect_aws_credentials import get_aws_secrets_from_env
from pre_commit_hooks.detect_aws_credentials import get_aws_secrets_from_file
from pre_commit_hooks.detect_aws_credentials import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('env_vars', 'values'),
    (
        ({}, set()),
        ({'AWS_PLACEHOLDER_KEY': '/foo'}, set()),
        ({'AWS_CONFIG_FILE': '/foo'}, {'/foo'}),
        ({'AWS_CREDENTIAL_FILE': '/foo'}, {'/foo'}),
        ({'AWS_SHARED_CREDENTIALS_FILE': '/foo'}, {'/foo'}),
        ({'BOTO_CONFIG': '/foo'}, {'/foo'}),
        ({'AWS_PLACEHOLDER_KEY': '/foo', 'AWS_CONFIG_FILE': '/bar'}, {'/bar'}),
        (
            {
                'AWS_PLACEHOLDER_KEY': '/foo', 'AWS_CONFIG_FILE': '/bar',
                'AWS_CREDENTIAL_FILE': '/baz',
            },
            {'/bar', '/baz'},
        ),
        (
            {
                'AWS_CONFIG_FILE': '/foo', 'AWS_CREDENTIAL_FILE': '/bar',
                'AWS_SHARED_CREDENTIALS_FILE': '/baz',
            },
            {'/foo', '/bar', '/baz'},
        ),
    ),
)
def test_get_aws_credentials_file_from_env(env_vars, values):
    with patch.dict('os.environ', env_vars, clear=True):
        assert get_aws_cred_files_from_env() == values


@pytest.mark.parametrize(
    ('env_vars', 'values'),
    (
        ({}, set()),
        ({'AWS_PLACEHOLDER_KEY': 'foo'}, set()),
        ({'AWS_SECRET_ACCESS_KEY': 'foo'}, {'foo'}),
        ({'AWS_SECURITY_TOKEN': 'foo'}, {'foo'}),
        ({'AWS_SESSION_TOKEN': 'foo'}, {'foo'}),
        ({'AWS_SESSION_TOKEN': ''}, set()),
        ({'AWS_SESSION_TOKEN': 'foo', 'AWS_SECURITY_TOKEN': ''}, {'foo'}),
        (
            {'AWS_PLACEHOLDER_KEY': 'foo', 'AWS_SECRET_ACCESS_KEY': 'bar'},
            {'bar'},
        ),
        (
            {'AWS_SECRET_ACCESS_KEY': 'foo', 'AWS_SECURITY_TOKEN': 'bar'},
            {'foo', 'bar'},
        ),
    ),
)
def test_get_aws_secrets_from_env(env_vars, values):
    """Test that reading secrets from environment variables works."""
    with patch.dict('os.environ', env_vars, clear=True):
        assert get_aws_secrets_from_env() == values


@pytest.mark.parametrize(
    ('filename', 'expected_keys'),
    (
        (
            'aws_config_with_secret.ini',
            {'z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb'},
        ),
        ('aws_config_with_session_token.ini', {'foo'}),
        (
            'aws_config_with_secret_and_session_token.ini',
            {'z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb', 'foo'},
        ),
        (
            'aws_config_with_multiple_sections.ini',
            {
                '7xebzorgm5143ouge9gvepxb2z70bsb2rtrh099e',
                'z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb',
                'ixswosj8gz3wuik405jl9k3vdajsnxfhnpui38ez',
                'foo',
            },
        ),
        ('aws_config_without_secrets.ini', set()),
        ('aws_config_without_secrets_with_spaces.ini', set()),
        ('nonsense.txt', set()),
        ('ok_json.json', set()),
    ),
)
def test_get_aws_secrets_from_file(filename, expected_keys):
    """Test that reading secrets from files works."""
    keys = get_aws_secrets_from_file(get_resource_path(filename))
    assert keys == expected_keys


@pytest.mark.parametrize(
    ('filename', 'expected_retval'),
    (
        ('aws_config_with_secret.ini', 1),
        ('aws_config_with_session_token.ini', 1),
        ('aws_config_with_multiple_sections.ini', 1),
        ('aws_config_without_secrets.ini', 0),
        ('aws_config_without_secrets_with_spaces.ini', 0),
        ('nonsense.txt', 0),
        ('ok_json.json', 0),
    ),
)
def test_detect_aws_credentials(filename, expected_retval):
    # with a valid credentials file
    ret = main((
        get_resource_path(filename),
        '--credentials-file',
        'testing/resources/aws_config_with_multiple_sections.ini',
    ))
    assert ret == expected_retval


def test_allows_arbitrarily_encoded_files(tmpdir):
    src_ini = tmpdir.join('src.ini')
    src_ini.write(
        '[default]\n'
        'aws_access_key_id=AKIASDFASDF\n'
        'aws_secret_Access_key=9018asdf23908190238123\n',
    )
    arbitrary_encoding = tmpdir.join('f')
    arbitrary_encoding.write_binary(b'\x12\x9a\xe2\xf2')
    ret = main((str(arbitrary_encoding), '--credentials-file', str(src_ini)))
    assert ret == 0


@patch('pre_commit_hooks.detect_aws_credentials.get_aws_secrets_from_file')
@patch('pre_commit_hooks.detect_aws_credentials.get_aws_secrets_from_env')
def test_non_existent_credentials(mock_secrets_env, mock_secrets_file, capsys):
    """Test behavior with no configured AWS secrets."""
    mock_secrets_env.return_value = set()
    mock_secrets_file.return_value = set()
    ret = main((
        get_resource_path('aws_config_without_secrets.ini'),
        '--credentials-file=testing/resources/credentailsfilethatdoesntexist',
    ))
    assert ret == 2
    out, _ = capsys.readouterr()
    assert out == (
        'No AWS keys were found in the configured credential files '
        'and environment variables.\nPlease ensure you have the '
        'correct setting for --credentials-file\n'
    )


@patch('pre_commit_hooks.detect_aws_credentials.get_aws_secrets_from_file')
@patch('pre_commit_hooks.detect_aws_credentials.get_aws_secrets_from_env')
def test_non_existent_credentials_with_allow_flag(
        mock_secrets_env, mock_secrets_file,
):
    mock_secrets_env.return_value = set()
    mock_secrets_file.return_value = set()
    ret = main((
        get_resource_path('aws_config_without_secrets.ini'),
        '--credentials-file=testing/resources/credentailsfilethatdoesntexist',
        '--allow-missing-credentials',
    ))
    assert ret == 0
