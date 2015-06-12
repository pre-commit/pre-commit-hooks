from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os

from six.moves import configparser


def get_your_keys(credentials_file):
    """ reads the secret keys in your credentials file in order to be able to look
    for them in the submitted code.
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


def check_file_for_aws_keys(filename, keys):
    with open(filename, 'r') as content:
        # naively match the entire file, chances be so slim
        # of random characters matching your flipping key.
        text_body = content.read()
        if any(key in text_body for key in keys):
            return 1
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument(
        "--credentials-file",
        default='~/.aws/credentials',
        help="location of aws credentials file from which to get the secret "
             "keys we're looking for",
    )
    args = parser.parse_args(argv)
    keys = get_your_keys(args.credentials_file)
    if not keys:
        return 2

    retv = 0
    for filename in args.filenames:
        retv |= check_file_for_aws_keys(filename, keys)
    return retv


if __name__ == '__main__':
    exit(main())
