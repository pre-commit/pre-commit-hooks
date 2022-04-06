from __future__ import annotations

import argparse
import os.path
from typing import Sequence

from pre_commit_hooks.util import cmd_output


CONFLICT_PATTERNS = [
    b'<<<<<<< ',
    b'======= ',
    b'=======\r\n',
    b'=======\n',
    b'>>>>>>> ',
]


def is_in_merge() -> bool:
    git_dir = cmd_output('git', 'rev-parse', '--git-dir').rstrip()
    return (
        os.path.exists(os.path.join(git_dir, 'MERGE_MSG')) and
        (
            os.path.exists(os.path.join(git_dir, 'MERGE_HEAD')) or
            os.path.exists(os.path.join(git_dir, 'rebase-apply')) or
            os.path.exists(os.path.join(git_dir, 'rebase-merge'))
        )
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--assume-in-merge', action='store_true')
    args = parser.parse_args(argv)

    if not is_in_merge() and not args.assume_in_merge:
        return 0

    retcode = 0
    for filename in args.filenames:
        with open(filename, 'rb') as inputfile:
            for i, line in enumerate(inputfile, start=1):
                for pattern in CONFLICT_PATTERNS:
                    if line.startswith(pattern):
                        print(
                            f'{filename}:{i}: Merge conflict string '
                            f'{pattern.strip().decode()!r} found',
                        )
                        retcode = 1

    return retcode


if __name__ == '__main__':
    raise SystemExit(main())
