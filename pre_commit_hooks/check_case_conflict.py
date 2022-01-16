from __future__ import annotations

import argparse
from typing import Iterable
from typing import Iterator
from typing import Sequence

from pre_commit_hooks.util import added_files
from pre_commit_hooks.util import cmd_output


def lower_set(iterable: Iterable[str]) -> set[str]:
    return {x.lower() for x in iterable}


def parents(file: str) -> Iterator[str]:
    path_parts = file.split('/')
    path_parts.pop()
    while path_parts:
        yield '/'.join(path_parts)
        path_parts.pop()


def directories_for(files: set[str]) -> set[str]:
    return {parent for file in files for parent in parents(file)}


def find_conflicting_filenames(filenames: Sequence[str]) -> int:
    repo_files = set(cmd_output('git', 'ls-files').splitlines())
    repo_files |= directories_for(repo_files)
    relevant_files = set(filenames) | added_files()
    relevant_files |= directories_for(relevant_files)
    repo_files -= relevant_files
    retv = 0

    # new file conflicts with existing file
    conflicts = lower_set(repo_files) & lower_set(relevant_files)

    # new file conflicts with other new file
    lowercase_relevant_files = lower_set(relevant_files)
    for filename in set(relevant_files):
        if filename.lower() in lowercase_relevant_files:
            lowercase_relevant_files.remove(filename.lower())
        else:
            conflicts.add(filename.lower())

    if conflicts:
        conflicting_files = [
            x for x in repo_files | relevant_files
            if x.lower() in conflicts
        ]
        for filename in sorted(conflicting_files):
            print(f'Case-insensitivity conflict found: {filename}')
        retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )

    args = parser.parse_args(argv)

    return find_conflicting_filenames(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
