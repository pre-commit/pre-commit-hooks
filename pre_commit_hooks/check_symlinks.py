from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import os.path


def check_symlinks(argv=None):
    parser = argparse.ArgumentParser(description='Checks for broken symlinks.')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        if (
                os.path.islink(filename) and
                not os.path.exists(filename)
        ):  # pragma: no cover (symlink support required)
            print('{0}: Broken symlink'.format(filename))
            retv = 1

    return retv


if __name__ == '__main__':
    exit(check_symlinks())
