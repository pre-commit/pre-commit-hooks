from __future__ import print_function

import argparse
import os.path
from typing import Optional
from typing import Sequence


CONFLICT_PATTERNS = [
    b'<<<<<<< ',
    b'======= ',
    b'=======\n',
    b'>>>>>>> ',
]
WARNING_MSG = 'Merge conflict string "{0}" found in {1}:{2}'


def is_in_merge():  # type: () -> int
    return (
        os.path.exists(os.path.join('.git', 'MERGE_MSG')) and
        (
            os.path.exists(os.path.join('.git', 'MERGE_HEAD')) or
            os.path.exists(os.path.join('.git', 'rebase-apply')) or
            os.path.exists(os.path.join('.git', 'rebase-merge'))
        )
    )


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
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
                        print(WARNING_MSG.format(
                            pattern.decode(), filename, i + 1,
                        ))
                        retcode = 1

    return retcode


if __name__ == '__main__':
    exit(main())
