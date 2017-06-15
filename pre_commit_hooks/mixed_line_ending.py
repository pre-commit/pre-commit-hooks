import argparse
import sys

from enum import Enum


class LineEnding(Enum):
    CRLF = '\r\n', '\\r\\n', 'crlf'
    LF = '\n', '\\n', 'lf'

    def __init__(self, str, strPrint, optName):
        self.str = str
        self.strPrint = strPrint
        self.optName = optName


def mixed_line_ending(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--fix',
        choices=['auto', 'no'] + [m.optName for m in LineEnding],
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
