from __future__ import print_function

import argparse
import io
import sys


def detect_private_key(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    private_key_files = []

    for filename in args.filenames:
        with io.open(filename, 'r') as f:
            content = f.read()
            if 'BEGIN RSA PRIVATE KEY' in content:
                private_key_files.append(content)
            if 'BEGIN DSA PRIVATE KEY' in content:
                private_key_files.append(content)

    if private_key_files:
        for private_key_file in private_key_files:
            print('Private key found: {0}'.format(private_key_file))
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(detect_private_key())
