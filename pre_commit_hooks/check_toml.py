from __future__ import annotations

import argparse
import sys
from typing import Sequence

if sys.version_info >= (3, 11):  # pragma: >=3.11 cover
    import tomllib
else:  # pragma: <3.11 cover
    import tomli as tomllib


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, mode='rb') as fp:
                tomllib.load(fp)
        except tomllib.TOMLDecodeError as exc:
            print(f'{filename}: {exc}')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
