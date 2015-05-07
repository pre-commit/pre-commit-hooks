from __future__ import print_function

import argparse
import os.path
import sys

CONFLICT_PATTERNS = [
    '<<<<<<< ',
    '======= ',
    '=======\n',
    '>>>>>>> '
]
WARNING_MSG = 'Merge conflict string "{0}" found in {1}:{2}'


def is_in_merge():
    return (
        os.path.exists(os.path.join('.git', 'MERGE_MSG')) and
        os.path.exists(os.path.join('.git', 'MERGE_HEAD'))
    )


def detect_merge_conflict(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    if not is_in_merge():
        return 0

    retcode = 0
    for filename in args.filenames:
        with open(filename) as inputfile:
            for i, line in enumerate(inputfile):
                for pattern in CONFLICT_PATTERNS:
                    if line.startswith(pattern):
                        print(WARNING_MSG.format(pattern, filename, i + 1))
                        retcode = 1

    return retcode

if __name__ == '__main__':
    sys.exit(detect_merge_conflict())
