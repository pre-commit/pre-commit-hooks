from __future__ import print_function

import argparse
import re
import sys


def validate_files(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--django', default=False, action='store_true',
        help='Use Django-style test naming pattern (test*.py)'
    )
    args = parser.parse_args(argv)

    retcode = 0
    test_name_pattern = '.*_test.py'
    if args.django:
        test_name_pattern = 'test.*.py'
    for filename in args.filenames:
        if (
                not re.match(test_name_pattern, filename) and
                not filename.endswith('__init__.py') and
                not filename.endswith('/conftest.py')
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
