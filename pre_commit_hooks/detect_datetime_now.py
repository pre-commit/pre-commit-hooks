from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check if datetime.now is being used.')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    for filename in args.filenames:
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                if b'datetime.now()' in f.read():
                    return 1

    return 0


if __name__ == '__main__':
    exit(main())
