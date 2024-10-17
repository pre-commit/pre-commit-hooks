from __future__ import annotations

import argparse
import os.path
import re
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    mutex = parser.add_mutually_exclusive_group()
    mutex.add_argument(
        '--pytest',
        dest='pattern',
        action='store_const',
        const=r'^tests\/(?:[a-zA-Z0-9_]+\/)*tests[a-zA-Z0-9_]*\.py$',
        default=r'^tests\/(?:[a-zA-Z0-9_]+\/)*tests[a-zA-Z0-9_]*\.py$',
        help='(the default) ensure tests match %(const)s',
    )
    args = parser.parse_args(argv)

    retcode = 0
    reg = re.compile(args.pattern)
    for filename in args.filenames:
        base = os.path.basename(filename)
        print(base)
        if (
                not reg.fullmatch(base) and
                not base == '.*/__init__.py' and
                not base == '.*/conftest.py' and
                not base == '.*/models.py'

        ):
            retcode = 1
            print(f'{filename} does not match pattern "{args.pattern}"')

    return retcode


if __name__ == '__main__':
    raise SystemExit(main())
