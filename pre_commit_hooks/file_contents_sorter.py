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
from typing import Any
from typing import Callable
from typing import IO
from typing import Iterable
from typing import Sequence

PASS = 0
FAIL = 1


class Line:
    """Wrapper to ignore end-of-line characters for sorting and comparison"""

    def __init__(self, value: bytes, eol: bytes):
        self._value = value
        # Add an EOL if none present (can only happen to the last line)
        if not self._value.endswith(b'\n'):
            self._value += eol

    def without_eol(self) -> bytes:
        return self._value.rstrip(b'\n\r')

    def unwrap(self) -> bytes:
        return self._value

    @classmethod
    def key(
        cls,
        key: Callable[[bytes], Any] | None = None,
    ) -> Callable[[Line], Any]:
        if key is None:
            return cls.without_eol
        else:
            def eol_key(val: Line) -> Any:
                return key(val.without_eol())

            return eol_key

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Line):
            return NotImplemented
        return self.without_eol().__eq__(o.without_eol())

    def __hash__(self) -> int:
        return self.without_eol().__hash__()


def guess_eol(lines: list[bytes]) -> bytes:
    if len(lines) == 0:
        return b'\n'

    for eol in [b'\r\n', b'\n']:
        if lines[0].endswith(eol):
            return eol

    # Prefer '\n' if the first (only) line does not have a line ending
    return b'\n'


def sort_file_contents(
    f: IO[bytes],
    key: Callable[[bytes], Any] | None,
    *,
    unique: bool = False,
) -> int:
    before = list(f)
    eol = guess_eol(before)
    lines: Iterable[Line] = (
        Line(line, eol) for line in before if line.strip()
    )
    if unique:
        lines = set(lines)
    after = sorted(lines, key=Line.key(key))

    before_string = b''.join(before)
    after_string = b''.join(line.unwrap() for line in after)

    if before_string == after_string:
        return PASS
    else:
        f.seek(0)
        f.write(after_string)
        f.truncate()
        return FAIL


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='Files to sort')
    parser.add_argument(
        '--ignore-case',
        action='store_const',
        const=bytes.lower,
        default=None,
        help='fold lower case to upper case characters',
    )
    parser.add_argument(
        '--unique',
        action='store_true',
        help='ensure each line is unique',
    )
    args = parser.parse_args(argv)

    retv = PASS

    for arg in args.filenames:
        with open(arg, 'rb+') as file_obj:
            ret_for_file = sort_file_contents(
                file_obj, key=args.ignore_case, unique=args.unique,
            )

            if ret_for_file:
                print(f'Sorting {arg}')

            retv |= ret_for_file

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
