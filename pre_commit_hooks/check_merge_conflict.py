from __future__ import annotations

import argparse
import os.path
from collections.abc import Sequence

from pre_commit_hooks.util import cmd_output


CONFLICT_PATTERNS = [
    b'<<<<<<< ',
    b'=======',
    b'>>>>>>> ',
]
N = len(CONFLICT_PATTERNS)


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
            expected_conflict_pattern_index = 0
            for i, line in enumerate(inputfile, start=1):
                # Look for conflict patterns in order
                if line.startswith(
                    CONFLICT_PATTERNS[expected_conflict_pattern_index],
                ):
                    expected_conflict_pattern_index += 1
                    if expected_conflict_pattern_index == N:
                        print(
                            f"{filename}:{i}: Merge conflict string "
                            f"{CONFLICT_PATTERNS[-1].strip().decode()!r} "
                            f"found",
                        )
                        retcode = 1
                        break
    return retcode


if __name__ == '__main__':
    raise SystemExit(main())
