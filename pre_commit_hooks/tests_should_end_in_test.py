from __future__ import print_function

import argparse
import os.path
import re
import sys
from typing import Optional
from typing import Sequence


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--django', default=False, action='store_true',
        help='Use Django-style test naming pattern (test*.py)',
    )

    parser.add_argument(
        '--exclude', default='facto.*.py',
        help='Use to exclude a certain pattern from check default to factory (fact*.py)',
    )
    args = parser.parse_args(argv)

    retcode = 0
    test_name_pattern = 'test.*.py' if args.django else '.*_test.py'
    for filename in args.filenames:
        base = os.path.basename(filename)
        if (
                not re.match(test_name_pattern, base) and
                not re.match(args.exclude, base) and
                not base == '__init__.py' and
                not base == 'conftest.py'
        ):
            retcode = 1
            print(
                '{} does not match pattern "{}"'.format(
                    filename, test_name_pattern,
                ),
            )

    return retcode


if __name__ == '__main__':
    sys.exit(main())
