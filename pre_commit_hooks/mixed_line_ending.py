import argparse
import logging
import os
import re
import sys

from enum import Enum


class LineEnding(Enum):
    CR = '\r', '\\r', 'cr', re.compile(r'\r', re.DOTALL)
    CRLF = '\r\n', '\\r\\n', 'crlf', re.compile(r'\r\n', re.DOTALL)
    LF = '\n', '\\n', 'lf', re.compile(r'(?<!\r)\n', re.DOTALL)

    def __init__(self, string, str_print, opt_name, regex):
        self.string = string
        self.str_print = str_print
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
    MIXED_MOSTLY_CRLF = True, LineEnding.CRLF
    MIXED_MOSTLY_LF = True, LineEnding.LF
    NOT_MIXED = False, None
    UNKNOWN = False, None

    def __init__(self, mle_found, line_ending_enum):
        self.mle_found = mle_found
        self.line_ending_enum = line_ending_enum


VERBOSE_OPTION_TO_LOGGING_SEVERITY = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


ANY_LINE_ENDING_PATTERN = re.compile(
    # match either
    '(' +
    # \r\n
    LineEnding.CRLF.regex.pattern +
    # or \n
    '|' + LineEnding.LF.regex.pattern +
    # or \r
    '|' + LineEnding.CR.regex.pattern +
    ')'
)


def mixed_line_ending(argv=None):
    options = _parse_arguments(argv)

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=options['logging_severity'])
    logging.debug('mixed_line_ending: options = %s', options)

    _check_filenames(options['filenames'])

    fix_option = options['fix']

    if fix_option == MixedLineEndingOption.NO:
        logging.info('No conversion asked')

        return 0
    elif fix_option == MixedLineEndingOption.AUTO:
        for filename in options['filenames']:
            detect_result = _detect_line_ending(filename)

            logging.debug('mixed_line_ending: detect_result = %s',
                          detect_result)

            if detect_result.mle_found:
                le_enum = detect_result.line_ending_enum

                logging.info('The file %s has mixed line ending with a '
                             'majority of "%s". Converting to "%s"', filename,
                             le_enum.str_print, le_enum.str_print)

                _convert_line_ending(filename, le_enum.string)

                return 1
            elif detect_result == MixedLineDetection.NOT_MIXED:
                logging.info('The file %s has no mixed line ending', filename)

                return 0
            elif detect_result == MixedLineDetection.UNKNOWN:
                logging.info('Could not define most frequent line ending in '
                             'file %s. File skiped.', filename)

                return 0

    # when a line ending character is forced with --fix option
    else:
        line_ending_enum = fix_option.line_ending_enum

        logging.info('Force line ending to "%s"', line_ending_enum.str_print)

        for filename in options['filenames']:
            _convert_line_ending(filename, line_ending_enum.string)

        return 1

    return 0


def _parse_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--fix',
        choices=[m.opt_name for m in MixedLineEndingOption],
        default=MixedLineEndingOption.AUTO.opt_name,
        help='Replace line ending with the specified. Default is "auto"')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument(
        '-v',
        '--verbose',
        action="count",
        default=0,
        help='Increase output verbosity')
    args = parser.parse_args(argv)

    fix = None
    if args.fix == MixedLineEndingOption.AUTO.opt_name:
        fix = MixedLineEndingOption.AUTO
    elif args.fix == MixedLineEndingOption.NO.opt_name:
        fix = MixedLineEndingOption.NO
    elif args.fix == MixedLineEndingOption.CRLF.opt_name:
        fix = MixedLineEndingOption.CRLF
    elif args.fix == MixedLineEndingOption.LF.opt_name:
        fix = MixedLineEndingOption.LF

    args.verbose = min(args.verbose, 2)
    severity = VERBOSE_OPTION_TO_LOGGING_SEVERITY.get(args.verbose)

    options = {'fix': fix, 'filenames': args.filenames,
               'logging_severity': severity}

    return options


def _check_filenames(filenames):
    logging.debug('_check_filenames: filenames = %s', filenames)

    for filename in filenames:
        if not os.path.isfile(filename):
            raise IOError('The file "{}" does not exist'.format(filename))


def _detect_line_ending(filename):
    f = open(filename, 'r')
    buf = f.read()
    f.close()

    crlf_nb = len(LineEnding.CRLF.regex.findall(buf))
    lf_nb = len(LineEnding.LF.regex.findall(buf))

    crlf_found = crlf_nb > 0
    lf_found = lf_nb > 0

    logging.debug('_detect_line_ending: crlf_nb = %d, lf_nb = %d, '
                  'crlf_found = %s, lf_found = %s',
                  crlf_nb, lf_nb, crlf_found, lf_found)

    if crlf_nb == lf_nb:
        return MixedLineDetection.UNKNOWN

    if crlf_found ^ lf_found:
        return MixedLineDetection.NOT_MIXED

    if crlf_nb > lf_nb:
        return MixedLineDetection.MIXED_MOSTLY_CRLF
    else:
        return MixedLineDetection.MIXED_MOSTLY_LF


def _convert_line_ending(filename, line_ending):
    # read the file
    fin = open(filename, 'r')
    bufin = fin.read()
    fin.close()

    # convert line ending
    bufout = ANY_LINE_ENDING_PATTERN.sub(line_ending, bufin)

    # write the result in the file
    fout = open(filename, 'w')
    fout.write(bufout)
    fout.close()


if __name__ == '__main__':
    sys.exit(mixed_line_ending())
