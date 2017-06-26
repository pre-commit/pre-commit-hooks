import argparse
import os
import re
import sys

from enum import Enum


class CLIOption(Enum):
    def __init__(self, optName):
        self.optName = optName


class LineEnding(CLIOption):
    CR = '\r', '\\r', 'cr'
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


class MixedLineDetection(Enum):
    MIXED_MOSTLY_CRLF = True, LineEnding.CRLF.string
    MIXED_MOSTLY_LF = True, LineEnding.LF.string
    NOT_MIXED = False, None
    UNKNOWN = False, None

    def __init__(self, conversion, line_ending_char):
        self.conversion = conversion
        self.line_ending_char = line_ending_char


# Matches CRLF
CRLF_PATTERN = re.compile(LineEnding.CRLF.string, re.DOTALL)
# Matches LF (without preceding CR)
LF_PATTERN = re.compile('(?<!' + LineEnding.CR.strPrint + ')' + LineEnding.LF.strPrint, re.DOTALL)


def mixed_line_ending(argv=None):
    options = _parse_arguments(argv)

    print(options)

    _check_filenames(options['filenames'])

    for filename in options['filenames']:
        print(_detect_line_ending(filename))

    return 0


def _parse_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--fix',
        choices=[m.optName for m in MixedLineEndingOption],
        default='auto',
        help='Replace line ending with the specified. Default is "auto"')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
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

    options = {'fix': fix, 'filenames': args.filenames, 'verbose': args.verbose}

    return options


def _check_filenames(filenames):
    for filename in filenames:
        if not os.path.isfile(filename):
            raise IOError('The file "{}" does not exist'.format(filename))


def _detect_line_ending(filename):
    f = open(filename, 'r')
    buf = f.read()

    crlf_nb = len(CRLF_PATTERN.findall(buf))
    lf_nb = len(LF_PATTERN.findall(buf))

    crlf_found = crlf_nb > 0
    lf_found = lf_nb > 0

    if crlf_nb == lf_nb:
        return MixedLineDetection.UNKNOWN

    if crlf_found ^ lf_found:
        return MixedLineDetection.NOT_MIXED

    if crlf_nb > lf_nb:
        return MixedLineDetection.MIXED_MOSTLY_CRLF
    else:
        return MixedLineDetection.MIXED_MOSTLY_LF


if __name__ == '__main__':
    sys.exit(mixed_line_ending())
