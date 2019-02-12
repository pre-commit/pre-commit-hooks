from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set

from six.moves import configparser


def get_aws_cred_files_from_env():  # type: () -> Set[str]
    """Extract credential file paths from environment variables."""
    return {
        os.environ[env_var]
        for env_var in (
            'AWS_CONFIG_FILE', 'AWS_CREDENTIAL_FILE',
            'AWS_SHARED_CREDENTIALS_FILE', 'BOTO_CONFIG',
        )
        if env_var in os.environ
    }


def get_aws_secrets_from_env():  # type: () -> Set[str]
    """Extract AWS secrets from environment variables."""
    keys = set()
    for env_var in (
        'AWS_SECRET_ACCESS_KEY', 'AWS_SECURITY_TOKEN', 'AWS_SESSION_TOKEN',
    ):
        if env_var in os.environ:
            keys.add(os.environ[env_var])
    return keys


def get_aws_secrets_from_file(credentials_file):  # type: (str) -> Set[str]
    """Extract AWS secrets from configuration files.

    Read an ini-style configuration file and return a set with all found AWS
    secret access keys.
    """
    aws_credentials_file_path = os.path.expanduser(credentials_file)
    if not os.path.exists(aws_credentials_file_path):
        return set()

    parser = configparser.ConfigParser()
    try:
        parser.read(aws_credentials_file_path)
    except configparser.MissingSectionHeaderError:
        return set()

    keys = set()
    for section in parser.sections():
        for var in (
            'aws_secret_access_key', 'aws_security_token',
            'aws_session_token',
        ):
            try:
                key = parser.get(section, var).strip()
                if key:
                    keys.add(key)
            except configparser.NoOptionError:
                pass
    return keys


def check_file_for_aws_keys(filenames, keys):
    # type: (Sequence[str], Set[str]) -> List[Dict[str, str]]
    """Check if files contain AWS secrets.

    Return a list of all files containing AWS secrets and keys found, with all
    but the first four characters obfuscated to ease debugging.
    """
    bad_files = []

    for filename in filenames:
        with open(filename, 'r') as content:
            text_body = content.read()
            for key in keys:
                # naively match the entire file, low chance of incorrect
                # collision
                if key in text_body:
                    bad_files.append({
                        'filename': filename, 'key': key[:4] + '*' * 28,
                    })
    return bad_files


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='Filenames to run')
    parser.add_argument(
        '--credentials-file',
        dest='credentials_file',
        action='append',
        default=[
            '~/.aws/config', '~/.aws/credentials', '/etc/boto.cfg', '~/.boto',
        ],
        help=(
            'Location of additional AWS credential file from which to get '
            'secret keys. Can be passed multiple times.'
        ),
    )
    parser.add_argument(
        '--allow-missing-credentials',
        dest='allow_missing_credentials',
        action='store_true',
        help='Allow hook to pass when no credentials are detected.',
    )
    args = parser.parse_args(argv)

    credential_files = set(args.credentials_file)

    # Add the credentials files configured via environment variables to the set
    # of files to to gather AWS secrets from.
    credential_files |= get_aws_cred_files_from_env()

    keys = set()  # type: Set[str]
    for credential_file in credential_files:
        keys |= get_aws_secrets_from_file(credential_file)

    # Secrets might be part of environment variables, so add such secrets to
    # the set of keys.
    keys |= get_aws_secrets_from_env()

    if not keys and args.allow_missing_credentials:
        return 0

    if not keys:
        print(
            'No AWS keys were found in the configured credential files and '
            'environment variables.\nPlease ensure you have the correct '
            'setting for --credentials-file',
        )
        return 2

    bad_filenames = check_file_for_aws_keys(args.filenames, keys)
    if bad_filenames:
        for bad_file in bad_filenames:
            print('AWS secret found in {filename}: {key}'.format(**bad_file))
        return 1
    else:
        return 0


if __name__ == '__main__':
    exit(main())
