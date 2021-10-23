import argparse
import os.path
from typing import Optional
from typing import Sequence

from pre_commit_hooks.util import cmd_output


CONFLICT_PATTERNS = [
    b'<<<<<<< ',
    b'======= ',
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


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--assume-in-merge', action='store_true')
    args = parser.parse_args(argv)

    if not is_in_merge() and not args.assume_in_merge:
        return 0

    retcode = 0
    for filename in args.filenames:
        with open(filename, 'rb') as inputfile:
            for i, line in enumerate(inputfile):
                for pattern in CONFLICT_PATTERNS:
                    if line.startswith(pattern):
                        print(
                            f'Merge conflict string "{pattern.decode()}" '
                            f'found in {filename}:{i + 1}',
                        )
                        retcode = 1

    return retcode


if __name__ == '__main__':
    raise SystemExit(main())
