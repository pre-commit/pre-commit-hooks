from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io

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


def fix_encoding_pragma(f):
    first_line = f.readline()
    second_line = f.readline()
    old = f.read()
    f.seek(0)

    # Ok case: the file is empty
    if not (first_line + second_line + old).strip():
        return 0

    # Ok case: we specify pragma as the first line
    if first_line == expected_pragma:
        return 0

    # OK case: we have a shebang as first line and pragma on second line
    if first_line.startswith(b'#!') and second_line == expected_pragma:
        return 0

    # Otherwise we need to rewrite stuff!
    if first_line.startswith(b'#!'):
        if has_coding(second_line):
            f.write(first_line + expected_pragma + old)
        else:
            f.write(first_line + expected_pragma + second_line + old)
    elif has_coding(first_line):
        f.write(expected_pragma + second_line + old)
    else:
        f.write(expected_pragma + first_line + second_line + old)

    return 1


def main(argv=None):
    parser = argparse.ArgumentParser('Fixes the encoding pragma of python files')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with io.open(filename, 'r+b') as f:
            file_ret = fix_encoding_pragma(f)
            retv |= file_ret
            if file_ret:
                print('Added `{0}` to {1}'.format(
                    expected_pragma.strip(), filename,
                ))

    return retv

if __name__ == "__main__":
    exit(main())
