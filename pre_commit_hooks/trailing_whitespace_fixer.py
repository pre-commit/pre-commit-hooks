from __future__ import print_function

import argparse
import fileinput
import sys

from plumbum import local


def _fix_file(filename):
    for line in fileinput.input([filename], inplace=True):
        print(line.rstrip())


def fix_trailing_whitespace(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    bad_whitespace_files = local['grep'][
        ('-l', '[[:space:]]$') + tuple(args.filenames)
    ](retcode=None).strip().splitlines()

    if bad_whitespace_files:
        for bad_whitespace_file in bad_whitespace_files:
            print('Fixing {0}'.format(bad_whitespace_file))
            _fix_file(bad_whitespace_file)
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(fix_trailing_whitespace())
