import argparse
import os.path
import re
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--django', default=False, action='store_true',
        help='Use Django-style test naming pattern (test*.py)',
    )
    args = parser.parse_args(argv)

    retcode = 0
    test_name_pattern = r'test.*\.py' if args.django else r'.*_test\.py'
    for filename in args.filenames:
        base = os.path.basename(filename)
        if (
                not re.match(test_name_pattern, base) and
                not base == '__init__.py' and
                not base == 'conftest.py'
        ):
            retcode = 1
            print(f'{filename} does not match pattern "{test_name_pattern}"')

    return retcode


if __name__ == '__main__':
    raise SystemExit(main())
