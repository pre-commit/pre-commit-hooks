from __future__ import print_function

import argparse
import sys


def validate_files(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retcode = 0
    for filename in args.filenames:
        if (
                not filename.endswith('_test.py') and
                not filename.endswith('__init__.py') and
                not filename.endswith('/conftest.py')
        ):
            retcode = 1
            print('{0} does not end in _test.py'.format(filename))

    return retcode


if __name__ == '__main__':
    sys.exit(validate_files())
