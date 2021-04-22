import argparse
import os.path
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Sequence
from typing import Set

from pre_commit_hooks.util import added_files


def lower_set(iterable: Iterable[str]) -> Set[str]:
    return {x.lower() for x in iterable}


def parents(file: str) -> Iterator[str]:
    file = os.path.dirname(file)
    while file:
        yield file
        file = os.path.dirname(file)


def directories_for(files: Set[str]) -> Set[str]:
    return {parent for file in files for parent in parents(file)}


# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
ILLEGAL_NAMES = {
    'CON',
    'PRN',
    'AUX',
    'NUL',
    *(f'COM{i}' for i in range(1, 10)),
    *(f'LPT{i}' for i in range(1, 10)),
}


def find_illegal_windows_names(filenames: Sequence[str]) -> int:
    relevant_files = set(filenames) | added_files()
    relevant_files |= directories_for(relevant_files)
    retv = 0

    for filename in relevant_files:
        root = os.path.basename(filename)
        while '.' in root:
            root, _ = os.path.splitext(root)
        if root.lower() in lower_set(ILLEGAL_NAMES):
            print(f'Illegal name {filename}')
            retv = 1
    return retv


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )

    args = parser.parse_args(argv)

    return find_illegal_windows_names(args.filenames)


if __name__ == '__main__':
    exit(main())
