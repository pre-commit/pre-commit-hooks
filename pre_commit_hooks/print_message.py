from __future__ import print_function

import argparse
import sys

default_message = 'You failed to provide a message to the `print_message` pre-commit hook via the -m or --message arg'


def main(argv=[]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--message',
        dest='message',
        default=default_message,
        help='the message to display when this pre-commit hook is triggered',
    )
    parser.add_argument(
        '-f',
        '--fail',
        dest='outcome',
        action='store_const',
        const=1,
        default=0,
        help='use this flag to make the pre-commit hook fail if it is triggered',
    )
    args = parser.parse_args(argv)
    print(args.message)
    return args.outcome


if __name__ == '__main__':
    sys.exit(main())
