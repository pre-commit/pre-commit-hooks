from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os

from six.moves import configparser  # pylint: disable=import-error


def get_your_keys(credentials_file):
    """reads the secret keys in your credentials file in order to be able to
    look for them in the submitted code.
    """
    aws_credentials_file_path = os.path.expanduser(credentials_file)
    if not os.path.exists(aws_credentials_file_path):
        return None

    parser = configparser.ConfigParser()
    parser.read(aws_credentials_file_path)

    keys = set()
    for section in parser.sections():
        keys.add(parser.get(section, 'aws_secret_access_key'))
    return keys


def check_file_for_aws_keys(filenames, keys):
    bad_files = []

    for filename in filenames:
        with open(filename, 'r') as content:
            text_body = content.read()
            if any(key in text_body for key in keys):
                # naively match the entire file, low chance of incorrect collision
                bad_files.append(filename)

    return bad_files


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument(
        '--credentials-file',
        default='~/.aws/credentials',
        help=(
            'location of aws credentials file from which to get the secret '
            "keys we're looking for"
        ),
    )
    args = parser.parse_args(argv)
    keys = get_your_keys(args.credentials_file)
    if not keys:
        print(
            'No aws keys were configured at {0}\n'
            'Configure them with --credentials-file'.format(
                args.credentials_file,
            ),
        )
        return 2

    bad_filenames = check_file_for_aws_keys(args.filenames, keys)
    if bad_filenames:
        for bad_file in bad_filenames:
            print('AWS secret key found: {0}'.format(bad_file))
        return 1
    else:
        return 0

if __name__ == '__main__':
    exit(main())
