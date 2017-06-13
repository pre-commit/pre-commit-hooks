import argparse
import sys


def mixed_line_ending(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--fix',
        choices=['auto', 'crlf', 'lf', 'no'],
        default='auto',
        help='Replace line ending with the specified. Default is "auto"',
        nargs=1)
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help='Increase output verbosity')
    args = parser.parse_args(argv)

    print(args.fix)

    return 0


if __name__ == '__main__':
    sys.exit(mixed_line_ending())
