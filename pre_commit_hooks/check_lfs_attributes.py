from __future__ import annotations

import argparse
import subprocess
from typing import Sequence

from pre_commit_hooks.util import zsplit


def select_lfs_attr_files(filenames: set[str]) -> set[str]:  # pragma: no cover (lfs)
    """Select files tracked by git-lfs from the set."""
    if not filenames:
        return filenames

    check_attr = subprocess.run(
        ('git', 'check-attr', 'filter', '-z', '--stdin'),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        encoding='utf-8',
        check=True,
        input='\0'.join(filenames),
    )
    stdout = zsplit(check_attr.stdout)
    # stdout values are triplets:
    #   ['b.txt', 'filter', 'unspecified', 'a.bin', 'filter', 'lfs']
    return {stdout[i] for i in range(0, len(stdout), 3) if stdout[i + 2] == 'lfs'}


def select_lfs_tree_files(filenames: set[str]) -> set[str]:  # pragma: no cover
    """Select LSF files found in the tree."""
    if not filenames:
        return filenames

    output = subprocess.check_output(('git', 'lfs', 'ls-files', '-n'), text=True)
    lfs_files = set(output.split())

    return lfs_files & set(filenames)


def check_lfs_attributes(filenames: Sequence[str]) -> int:
    unique_filenames = set(filenames)

    lfs_attr_files = select_lfs_attr_files(unique_filenames)
    lfs_tree_files = select_lfs_tree_files(unique_filenames)

    retv = 0
    for filename in lfs_attr_files - lfs_tree_files:
        print(f'{filename} is tracked by LFS but added as a regular object')
        retv = 1
    for filename in lfs_tree_files - lfs_attr_files:
        print(f'{filename} is added as LFS object but not tracked')
        retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    args = parser.parse_args(argv)

    return check_lfs_attributes(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
