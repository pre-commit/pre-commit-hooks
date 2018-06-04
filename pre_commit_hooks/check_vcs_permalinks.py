from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import sys


GITHUB_NON_PERMALINK = re.compile(
    b'https?://(www\.)?github.com/[^/]+/[^/]+/blob/master/[^# ]+#',
)


def _check_filename(filename):
    retv = 0
    with open(filename, 'rb') as f:
        for i, line in enumerate(f, 1):
            if GITHUB_NON_PERMALINK.search(line):
                sys.stdout.write('{}:{}:'.format(filename, i))
                sys.stdout.flush()
                getattr(sys.stdout, 'buffer', sys.stdout).write(line)
                retv = 1
    return retv


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        retv |= _check_filename(filename)

    if retv:
        print()
        print('Non-permanent github link detected.')
        print('On any page on github press [y] to load a permalink.')
    return retv


if __name__ == '__main__':
    exit(main())
