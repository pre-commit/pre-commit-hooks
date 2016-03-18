from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            if f.read(3) == b'\xef\xbb\xbf':
                retv = 1
                print('{0}: Has a byte-order marker'.format(filename))

    return retv


if __name__ == '__main__':
    exit(main())
