from __future__ import annotations

import argparse
from collections.abc import Sequence

EM_DASH = '\N{EM DASH}'.encode()


def _fix_file(filename: str) -> bool:
    with open(filename, 'rb') as f:
        contents = f.read()
    new_contents = contents.replace(EM_DASH, b'-')
    if new_contents == contents:
        return False
    with open(filename, 'wb') as f:
        f.write(new_contents)
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        if _fix_file(filename):
            print(f'Fixing {filename}')
            retv = 1
    return retv


if __name__ == '__main__':
    raise SystemExit(main())
