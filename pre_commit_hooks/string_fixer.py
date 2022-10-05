from __future__ import annotations

import argparse
from typing import Sequence

from pre_commit_hooks.util_string_fixer import fix_strings_in_file_contents


def fix_strings(filename: str) -> int:
    with open(filename, encoding='UTF-8', newline='') as f:
        contents = f.read()

    new_contents = fix_strings_in_file_contents(contents)

    if contents != new_contents:
        with open(filename, 'w', encoding='UTF-8', newline='') as f:
            f.write(new_contents)
        return 1
    else:
        return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        return_value = fix_strings(filename)
        if return_value != 0:
            print(f'Fixing strings in {filename}')
        retv |= return_value

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
