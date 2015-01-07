from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import math
import os
import sys

from pre_commit_hooks.util import added_files


def find_large_added_files(filenames, maxkb):
    # Find all added files that are also in the list of files pre-commit tells
    # us about
    filenames = added_files() & set(filenames)

    retv = 0
    for filename in filenames:
        kb = int(math.ceil(os.stat(filename).st_size / 1024))
        if kb > maxkb:
            print('{0} ({1} KB) exceeds {2} KB.'.format(filename, kb, maxkb))
            retv = 1

    return retv


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.'
    )
    parser.add_argument(
        '--maxkb', type=int, default=500,
        help='Maxmimum allowable KB for added files',
    )

    args = parser.parse_args(argv)
    return find_large_added_files(args.filenames, args.maxkb)


if __name__ == '__main__':
    exit(main())
