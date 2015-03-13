from __future__ import print_function

import argparse
import sys

CONFLICT_PATTERNS = [
    '<<<<<<< ',
    '=======',
    '>>>>>>> '
]
WARNING_MSG = 'Merge conflict string "{0}" found in {1}:{2}'


def detect_merge_conflict(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retcode = 0
    for filename in args.filenames:
        with open(filename) as inputfile:
            for i, line in enumerate(inputfile):
                for pattern in CONFLICT_PATTERNS:
                    if line.startswith(pattern):
                        print(WARNING_MSG.format(pattern, filename, i))
                        retcode = 1

    return retcode

if __name__ == '__main__':
    sys.exit(detect_merge_conflict())
