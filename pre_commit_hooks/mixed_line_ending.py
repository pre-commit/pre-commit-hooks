import argparse
import sys

from enum import Enum


class CLIOption(Enum):
    def __init__(self, optName):
        self.optName = optName


class LineEnding(CLIOption):
    CRLF = '\r\n', '\\r\\n', 'crlf'
    LF = '\n', '\\n', 'lf'

    def __init__(self, string, strPrint, optName):
        self.string = string
        self.strPrint = strPrint
        self.optName = optName


class MixedLineEndingOption(CLIOption):
    AUTO = 'auto'
    NO = 'no'
    CRLF = LineEnding.CRLF.optName
    LF = LineEnding.LF.optName


def mixed_line_ending(argv=None):
    options = _parse_arguments(argv)

    print(options)

    return 0


def _parse_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--fix',
        choices=[m.optName for m in MixedLineEndingOption],
        default='auto',
        help='Replace line ending with the specified. Default is "auto"')
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help='Increase output verbosity')
    args = parser.parse_args(argv)

    fix = None
    if args.fix == 'auto':
        fix = MixedLineEndingOption.AUTO
    elif args.fix == 'no':
        fix = MixedLineEndingOption.NO
    elif args.fix == 'crlf':
        fix = MixedLineEndingOption.CRLF
    elif args.fix == 'lf':
        fix = MixedLineEndingOption.LF

    options = {'fix': fix, 'verbose': args.verbose}

    return options


if __name__ == '__main__':
    sys.exit(mixed_line_ending())
