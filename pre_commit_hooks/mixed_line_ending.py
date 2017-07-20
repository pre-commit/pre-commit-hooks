import argparse
import os
import re
import sys

from enum import Enum


class LineEnding(Enum):
    CR = b'\r', 'cr', re.compile(b'\r(?!\n)', re.DOTALL)
    CRLF = b'\r\n', 'crlf', re.compile(b'\r\n', re.DOTALL)
    LF = b'\n', 'lf', re.compile(b'(?<!\r)\n', re.DOTALL)

    def __init__(self, string, opt_name, regex):
        self.string = string
        self.str_print = repr(string)
        self.opt_name = opt_name
        self.regex = regex


class MixedLineEndingOption(Enum):
    AUTO = 'auto', None
    NO = 'no', None
    CRLF = LineEnding.CRLF.opt_name, LineEnding.CRLF
    LF = LineEnding.LF.opt_name, LineEnding.LF

    def __init__(self, opt_name, line_ending_enum):
        self.opt_name = opt_name
        self.line_ending_enum = line_ending_enum


class MixedLineDetection(Enum):
    NOT_MIXED = 1, False, None
    UNKNOWN = 2, False, None
    MIXED_MOSTLY_CRLF = 3, True, LineEnding.CRLF
    MIXED_MOSTLY_LF = 4, True, LineEnding.LF
    MIXED_MOSTLY_CR = 5, True, LineEnding.CR

    def __init__(self, index, mle_found, line_ending_enum):
        # TODO hack to prevent enum overriding
        self.index = index
        self.mle_found = mle_found
        self.line_ending_enum = line_ending_enum


ANY_LINE_ENDING_PATTERN = re.compile(
    b'(' + LineEnding.CRLF.regex.pattern +
    b'|' + LineEnding.LF.regex.pattern +
    b'|' + LineEnding.CR.regex.pattern + b')',
)


def mixed_line_ending(argv=None):
    options = _parse_arguments(argv)

    filenames = options['filenames']
    fix_option = options['fix']

    _check_filenames(filenames)

    if fix_option == MixedLineEndingOption.NO:
        return _process_no_fix(filenames)
    elif fix_option == MixedLineEndingOption.AUTO:
        return _process_fix_auto(filenames)
    # when a line ending character is forced with --fix option
    else:
        return _process_fix_force(filenames, fix_option.line_ending_enum)


def _parse_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--fix',
        choices=[m.opt_name for m in MixedLineEndingOption],
        default=MixedLineEndingOption.AUTO.opt_name,
        help='Replace line ending with the specified. Default is "auto"',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    fix, = (
        member for name, member
        in MixedLineEndingOption.__members__.items()
        if member.opt_name == args.fix
    )

    options = {
        'fix': fix, 'filenames': args.filenames,
    }

    return options


def _check_filenames(filenames):
    for filename in filenames:
        if not os.path.isfile(filename):
            raise IOError('The file "{}" does not exist'.format(filename))


def _detect_line_ending(filename):
    with open(filename, 'rb') as f:
        buf = f.read()

        le_counts = {}
        for le_enum in LineEnding:
            le_counts[le_enum] = len(le_enum.regex.findall(buf))

        mixed = False
        le_found_previously = False
        most_le = None
        max_le_count = 0

        for le, le_count in le_counts.items():
            le_found_cur = le_count > 0

            mixed |= le_found_previously and le_found_cur
            le_found_previously |= le_found_cur

            if le_count == max_le_count:
                most_le = None
            elif le_count > max_le_count:
                max_le_count = le_count
                most_le = le

        if not mixed:
            return MixedLineDetection.NOT_MIXED

        for mld in MixedLineDetection:
            if mld.line_ending_enum is not None \
               and mld.line_ending_enum == most_le:
                return mld

        return MixedLineDetection.UNKNOWN


def _process_no_fix(filenames):
    print('Checking if the files have mixed line ending.')

    mle_filenames = []
    for filename in filenames:
        detect_result = _detect_line_ending(filename)

        if detect_result.mle_found:
            mle_filenames.append(filename)

    mle_found = len(mle_filenames) > 0

    if mle_found:
        print(
            'The following files have mixed line endings:\n\t%s',
            '\n\t'.join(mle_filenames),
        )

    return 1 if mle_found else 0


def _process_fix_auto(filenames):
    mle_found = False

    for filename in filenames:
        detect_result = _detect_line_ending(filename)

        if detect_result == MixedLineDetection.NOT_MIXED:
            print('The file %s has no mixed line ending', filename)

            mle_found |= False
        elif detect_result == MixedLineDetection.UNKNOWN:
            print(
                'Could not define most frequent line ending in '
                'file %s. File skiped.', filename,
            )

            mle_found = True
        else:
            le_enum = detect_result.line_ending_enum

            print(
                'The file %s has mixed line ending with a '
                'majority of %s. Converting...', filename, le_enum.str_print,
            )

            _convert_line_ending(filename, le_enum.string)
            mle_found = True

            print(
                'The file %s has been converted to %s line ending.',
                filename, le_enum.str_print,
            )

    return 1 if mle_found else 0


def _process_fix_force(filenames, line_ending_enum):
    for filename in filenames:
        _convert_line_ending(filename, line_ending_enum.string)

        print(
            'The file %s has been forced to %s line ending.',
            filename, line_ending_enum.str_print,
        )

    return 1


def _convert_line_ending(filename, line_ending):
    with open(filename, 'rb+') as f:
        bufin = f.read()

        # convert line ending
        bufout = ANY_LINE_ENDING_PATTERN.sub(line_ending, bufin)

        # write the result in the file replacing the existing content
        f.seek(0)
        f.write(bufout)
        f.truncate()


if __name__ == '__main__':
    sys.exit(mixed_line_ending())
