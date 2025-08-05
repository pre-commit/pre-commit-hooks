"""
A very simple pre-commit hook that, when passed one or more filenames
as arguments, will sort the lines in those files.

An example use case for this: you have a deploy-allowlist.txt file
in a repo that contains a list of filenames that is used to specify
files to be included in a docker container. This file has one filename
per line. Various users are adding/removing lines from this file; using
this hook on that file should reduce the instances of git merge
conflicts and keep the file nicely ordered.
"""
from __future__ import annotations

import argparse
from collections.abc import Iterable
from collections.abc import Sequence
from typing import Any
from typing import Callable
from typing import IO

PASS = 0
FAIL = 1


def sort_file_contents(
    f: IO[bytes],
    key: Callable[[bytes], Any] | None,
    *,
    unique: bool = False,
) -> int:
    before = list(f)
    lines: Iterable[bytes] = (
        line.rstrip(b'\n\r') for line in before if line.strip()
    )
    if unique:
        lines = set(lines)
    after = sorted(lines, key=key)

    before_string = b''.join(before)
    after_string = b'\n'.join(after)

    if after_string:
        after_string += b'\n'

    if before_string == after_string:
        return PASS
    else:
        f.seek(0)
        f.write(after_string)
        f.truncate()
        return FAIL


def group_cases_together_key(s: bytes) -> tuple[bytes, bytes]:
    return s.lower(), s


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='Files to sort')

    mutex = parser.add_mutually_exclusive_group(required=False)
    mutex.add_argument(
        '--ignore-case',
        action='store_const',
        const=bytes.lower,
        default=None,
        help='fold lower case to upper case characters. this retains\n'
        'the original order of lines that differ only in case,\n'
        'so you probably want --group-cases-together instead.',
    )
    mutex.add_argument(
        '--group-cases-together',
        action='store_const',
        const=group_cases_together_key,
        default=None,
        help='group lines that differ only in case together,\n'
        'so e.g. `c`, `b`, `a`, and `B` are sorted to\n'
        '`a`, `B`, `b`, and `c` instead of `B`, `a`, `b`, and `c`.',
    )
    parser.add_argument(
        '--unique',
        action='store_true',
        help='ensure each line is unique',
    )

    args = parser.parse_args(argv)
    # we can't just use add_mutually_exclusive_group for this since
    # --unique is allowed with --group-cases-together
    if args.ignore_case and args.unique:
        parser.error(
            'argument --ignore-case: not allowed with argument --unique',
        )

    key = args.ignore_case or args.group_cases_together

    retv = PASS

    for arg in args.filenames:
        with open(arg, 'rb+') as file_obj:
            ret_for_file = sort_file_contents(
                file_obj, key=key, unique=args.unique,
            )

            if ret_for_file:
                print(f'Sorting {arg}')

            retv |= ret_for_file

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
