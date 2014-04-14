from __future__ import print_function

import argparse
import sys
from plumbum import local

from pre_commit_hooks.util import entry


@entry
def fix_trailing_whitespace(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    bad_whitespace_files = local['grep'][
        ('-l', '[[:space:]]$') + tuple(args.filenames)
    ](retcode=None).strip().splitlines()

    if bad_whitespace_files:
        for bad_whitespace_file in bad_whitespace_files:
            print('Fixing {0}'.format(bad_whitespace_file))
            local['sed']['-i', '-e', 's/[[:space:]]*$//', bad_whitespace_file]()
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(fix_trailing_whitespace())
