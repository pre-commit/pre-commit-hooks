from __future__ import annotations

import argparse
import math
import os
import subprocess
from typing import Sequence

from pre_commit_hooks.util import added_files
from pre_commit_hooks.util import zsplit


def filter_lfs_files(filenames: set[str]) -> None:  # pragma: no cover (lfs)
    """Remove files tracked by git-lfs from the set."""
    if not filenames:
        return

    check_attr = subprocess.run(
        ('git', 'check-attr', 'filter', '-z', '--stdin'),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        encoding='utf-8',
        check=True,
        input='\0'.join(filenames),
    )
    stdout = zsplit(check_attr.stdout)
    for i in range(0, len(stdout), 3):
        filename, filter_tag = stdout[i], stdout[i + 2]
        if filter_tag == 'lfs':
            filenames.remove(filename)


def find_large_added_files(
        filenames: Sequence[str],
        maxkb: int,
        *,
        enforce_all: bool = False,
) -> int:
    # Find all added files that are also in the list of files pre-commit tells
    # us about
    retv = 0
    filenames_filtered = set(filenames)
    filter_lfs_files(filenames_filtered)

    if not enforce_all:
        filenames_filtered &= added_files()

    for filename in filenames_filtered:
        kb = math.ceil(os.stat(filename).st_size / 1024)
        if kb > maxkb:
            print(f'{filename} ({kb} KB) exceeds {maxkb} KB.')
            retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    parser.add_argument(
        '--enforce-all', action='store_true',
        help='Enforce all files are checked, not just staged files.',
    )
    parser.add_argument(
        '--maxkb', type=int, default=500,
        help='Maximum allowable KB for added files',
    )
    args = parser.parse_args(argv)

    return find_large_added_files(
        args.filenames,
        args.maxkb,
        enforce_all=args.enforce_all,
    )


if __name__ == '__main__':
    raise SystemExit(main())
