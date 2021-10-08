#!/usr/bin/env python3
import argparse
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--max-lines',
        default=30,
        type=int,
        action='store',
        help='Maximum allowed number of lines',
    )
    args = parser.parse_args(argv)

    retcode = 0
    for filename in args.filenames:
        with open(filename) as file:
            file_content = file.readlines()
            number_of_lines = len(file_content)
            if number_of_lines > args.max_lines:
                print(
                    f'{filename} ({number_of_lines} lines) exceeds '
                    f'{args.max_lines} lines.',
                )
                retcode = 1

    return retcode


if __name__ == '__main__':
    exit(main())
