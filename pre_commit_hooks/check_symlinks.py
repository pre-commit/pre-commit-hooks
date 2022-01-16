from __future__ import annotations

import argparse
import os.path
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Checks for broken symlinks.')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        if (
                os.path.islink(filename) and
                not os.path.exists(filename)
        ):  # pragma: no cover (symlink support required)
            print(f'{filename}: Broken symlink')
            retv = 1

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
