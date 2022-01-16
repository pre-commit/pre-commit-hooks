from __future__ import annotations

import argparse
from typing import IO
from typing import NamedTuple
from typing import Sequence

DEFAULT_PRAGMA = b'# -*- coding: utf-8 -*-'


def has_coding(line: bytes) -> bool:
    if not line.strip():
        return False
    return (
        line.lstrip()[:1] == b'#' and (
            b'unicode' in line or
            b'encoding' in line or
            b'coding:' in line or
            b'coding=' in line
        )
    )


class ExpectedContents(NamedTuple):
    shebang: bytes
    rest: bytes
    # True: has exactly the coding pragma expected
    # False: missing coding pragma entirely
    # None: has a coding pragma, but it does not match
    pragma_status: bool | None
    ending: bytes

    @property
    def has_any_pragma(self) -> bool:
        return self.pragma_status is not False

    def is_expected_pragma(self, remove: bool) -> bool:
        expected_pragma_status = not remove
        return self.pragma_status is expected_pragma_status


def _get_expected_contents(
        first_line: bytes,
        second_line: bytes,
        rest: bytes,
        expected_pragma: bytes,
) -> ExpectedContents:
    ending = b'\r\n' if first_line.endswith(b'\r\n') else b'\n'

    if first_line.startswith(b'#!'):
        shebang = first_line
        potential_coding = second_line
    else:
        shebang = b''
        potential_coding = first_line
        rest = second_line + rest

    if potential_coding.rstrip(b'\r\n') == expected_pragma:
        pragma_status: bool | None = True
    elif has_coding(potential_coding):
        pragma_status = None
    else:
        pragma_status = False
        rest = potential_coding + rest

    return ExpectedContents(
        shebang=shebang, rest=rest, pragma_status=pragma_status, ending=ending,
    )


def fix_encoding_pragma(
        f: IO[bytes],
        remove: bool = False,
        expected_pragma: bytes = DEFAULT_PRAGMA,
) -> int:
    expected = _get_expected_contents(
        f.readline(), f.readline(), f.read(), expected_pragma,
    )

    # Special cases for empty files
    if not expected.rest.strip():
        # If a file only has a shebang or a coding pragma, remove it
        if expected.has_any_pragma or expected.shebang:
            f.seek(0)
            f.truncate()
            f.write(b'')
            return 1
        else:
            return 0

    if expected.is_expected_pragma(remove):
        return 0

    # Otherwise, write out the new file
    f.seek(0)
    f.truncate()
    f.write(expected.shebang)
    if not remove:
        f.write(expected_pragma + expected.ending)
    f.write(expected.rest)

    return 1


def _normalize_pragma(pragma: str) -> bytes:
    return pragma.encode().rstrip()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        'Fixes the encoding pragma of python files',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument(
        '--pragma', default=DEFAULT_PRAGMA, type=_normalize_pragma,
        help=(
            f'The encoding pragma to use.  '
            f'Default: {DEFAULT_PRAGMA.decode()}'
        ),
    )
    parser.add_argument(
        '--remove', action='store_true',
        help='Remove the encoding pragma (Useful in a python3-only codebase)',
    )
    args = parser.parse_args(argv)

    retv = 0

    if args.remove:
        fmt = 'Removed encoding pragma from {filename}'
    else:
        fmt = 'Added `{pragma}` to {filename}'

    for filename in args.filenames:
        with open(filename, 'r+b') as f:
            file_ret = fix_encoding_pragma(
                f, remove=args.remove, expected_pragma=args.pragma,
            )
            retv |= file_ret
            if file_ret:
                print(
                    fmt.format(pragma=args.pragma.decode(), filename=filename),
                )

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
