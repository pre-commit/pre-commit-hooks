from __future__ import print_function

import argparse
import sys
from typing import Any


def contains_tabs(filename):  # type: (str) -> bool
    with open(filename, mode='rb') as file_checked:
        return b'\t' in file_checked.read()


def removes_tabs_in_file(filename, whitespaces_count):
    # type: (str, int) -> None
    with open(filename, mode='rb') as file_processed:
        lines = file_processed.readlines()
    lines = [line.replace(b'\t', b' ' * whitespaces_count) for line in lines]
    with open(filename, mode='wb') as file_processed:
        for line in lines:
            file_processed.write(line)


def main(argv=None):  # type: (Any) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--whitespaces-count', type=int, required=True,
        help='number of whitespaces to substitute tabs with',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')

    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        if contains_tabs(filename):
            print('Substituting tabs in: {} by {} whitespaces'.format(
                filename, args.whitespaces_count,
            ))
            removes_tabs_in_file(filename, args.whitespaces_count)
            return_code = 1

    if return_code:
        print('')
        print('Tabs have been successfully removed. Now aborting the commit.')
        print(
            'You can check the changes made. Then simply '
            '"git add --update ." and re-commit',
        )
    return return_code


if __name__ == '__main__':
    sys.exit(main())
