"""Pre-commit hook to check that yaml files are sorted at the top-level.

Does not modify files. Simply parses and compares the stringified values of
each element of the top-level object.

This allows it to handle all kinds of cases
- lists of scalars
- dicts by top-level key
- lists of dicts by first key name
- lists of dicts with same keys by first value...
"""
from __future__ import annotations

import argparse
from itertools import tee
from typing import Any
from typing import Iterable
from typing import Sequence

import yaml


def is_sorted(iterable: Iterable[Any]) -> bool:
    a_iter, b_iter = tee(str(e) for e in iterable)
    next(b_iter, None)
    for a, b in zip(a_iter, b_iter):
        if a > b:
            print(f'Items ({a[:32]}..., {b[:32]}...)')
            return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retval = 0

    for filename in args.filenames:
        with open(filename) as fp:
            data = yaml.safe_load(fp)
        if not is_sorted(data):
            print(f'In file {filename}, items are out of order.')
            retval += 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
