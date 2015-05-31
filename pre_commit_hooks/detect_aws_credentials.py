from __future__ import print_function
from __future__ import unicode_literals

import argparse
import ConfigParser
import os


def get_your_keys(credentials_file, ignore_access_key=False):
    """ reads the keys in your credentials file in order to be able to look
    for them in the submitted code.
    """
    aws_credentials_file_path = os.path.expanduser(credentials_file)
    if not os.path.exists(aws_credentials_file_path):
        exit(2)

    parser = ConfigParser.ConfigParser()
    parser.read(aws_credentials_file_path)

    keys = set()
    for section in parser.sections():
        if not ignore_access_key:
            keys.add(parser.get(section, 'aws_access_key_id'))
        keys.add(parser.get(section, 'aws_secret_access_key'))
    return keys


def check_file_for_aws_keys(filename, keys):
    with open(filename, 'r') as content:
        # naively match the entire file, chances be so slim
        # of random characters matching your flipping key.
        for line in content:
            if any(key in line for key in keys):
                return 1
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument(
        "--credentials-file", 
        default='~/.aws/credentials',
        help="location of aws credentials file from which to get the keys "
              "we're looking for",
    )
    parser.add_argument(
        "--ignore-access-key", 
        action='store_true',
        help="if you would like to ignore access keys, as there is "
        "occasionally legitimate use for these.",
    )
    args = parser.parse_args(argv)
    ignore_access_key = args.ignore_access_key
    keys = get_your_keys(args.credentials_file,
                         ignore_access_key=ignore_access_key)

    retv = 0
    for filename in args.filenames:
        retv |= check_file_for_aws_keys(filename, keys)
    return retv


if __name__ == '__main__':
    exit(main())
