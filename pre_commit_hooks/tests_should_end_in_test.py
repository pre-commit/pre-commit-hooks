from __future__ import print_function

import argparse
import re
import sys
from os.path import basename


def validate_files(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--django', default=False, action='store_true',
        help='Use Django-style test naming pattern (test*.py)'
    )
    args = parser.parse_args(argv)

    retcode = 0
    test_name_pattern = 'test_.*.py' if args.django else '.*_test.py'
    for filename in args.filenames:
        base = basename(filename)
        if (
                not re.match(test_name_pattern, base) and
                not base == '__init__.py' and
                not base == 'conftest.py'
        ):
            retcode = 1
            print(
                '{0} does not match pattern "{1}"'.format(
                    filename, test_name_pattern
                )
            )

    return retcode


if __name__ == '__main__':
    sys.exit(validate_files())
