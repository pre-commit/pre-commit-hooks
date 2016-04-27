from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import collections

expected_pragma = b'# -*- coding: utf-8 -*-\n'


def has_coding(line):
    if not line.strip():
        return False
    return (
        line.lstrip()[0:1] == b'#' and (
            b'unicode' in line or
            b'encoding' in line or
            b'coding:' in line or
            b'coding=' in line
        )
    )


class ExpectedContents(collections.namedtuple(
        'ExpectedContents', ('shebang', 'rest', 'pragma_status'),
)):
    """
    pragma_status:
    - True: has exactly the coding pragma expected
    - False: missing coding pragma entirely
    - None: has a coding pragma, but it does not match
    """
    __slots__ = ()

    @property
    def has_any_pragma(self):
        return self.pragma_status is not False

    def is_expected_pragma(self, remove):
        expected_pragma_status = not remove
        return self.pragma_status is expected_pragma_status


def _get_expected_contents(first_line, second_line, rest):
    if first_line.startswith(b'#!'):
        shebang = first_line
        potential_coding = second_line
    else:
        shebang = b''
        potential_coding = first_line
        rest = second_line + rest

    if potential_coding == expected_pragma:
        pragma_status = True
    elif has_coding(potential_coding):
        pragma_status = None
    else:
        pragma_status = False
        rest = potential_coding + rest

    return ExpectedContents(
        shebang=shebang, rest=rest, pragma_status=pragma_status,
    )


def fix_encoding_pragma(f, remove=False):
    expected = _get_expected_contents(f.readline(), f.readline(), f.read())

    # Special cases for empty files
    if not expected.rest.strip():
        # If a file only has a shebang or a coding pragma, remove it
        if expected.has_any_pragma or expected.shebang:
            f.seek(0)
            f.truncate()
            f.write(b'')
            return 1
        else:
            return 0

    if expected.is_expected_pragma(remove):
        return 0

    # Otherwise, write out the new file
    f.seek(0)
    f.truncate()
    f.write(expected.shebang)
    if not remove:
        f.write(expected_pragma)
    f.write(expected.rest)

    return 1


def main(argv=None):
    parser = argparse.ArgumentParser('Fixes the encoding pragma of python files')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument(
        '--remove', action='store_true',
        help='Remove the encoding pragma (Useful in a python3-only codebase)',
    )
    args = parser.parse_args(argv)

    retv = 0

    if args.remove:
        fmt = 'Removed encoding pragma from {filename}'
    else:
        fmt = 'Added `{pragma}` to {filename}'

    for filename in args.filenames:
        with open(filename, 'r+b') as f:
            file_ret = fix_encoding_pragma(f, remove=args.remove)
            retv |= file_ret
            if file_ret:
                print(fmt.format(pragma=expected_pragma, filename=filename))

    return retv

if __name__ == "__main__":
    exit(main())
