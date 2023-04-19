from __future__ import annotations

import argparse
import os
from typing import IO
from typing import Sequence


def detect_eol_equence(file_obj: IO[bytes]) -> bytes:
    # readline() doesn't work because it doesn't get \r right
    eol_marker = b''
    last_was_eol = False
    while True:
        next = file_obj.read(1)
        if not next:
            return eol_marker if eol_marker else b'\n'

        if next in (b'\r\n', b'\r', b'\n'):
            eol_marker += next
            last_was_eol = True
        else:
            # normal character
            if last_was_eol:
                return eol_marker

    return b'\n'


def fix_file(file_obj: IO[bytes]) -> int:
    # Test for newline at end of file
    # Empty files will throw IOError here
    try:
        file_obj.seek(-1, os.SEEK_END)
    except OSError:
        return 0
    last_character = file_obj.read(1)
    # last_character will be '' for an empty file
    if last_character not in {b'\n', b'\r'} and last_character != b'':
        file_obj.seek(0, os.SEEK_SET)
        eol_seq = detect_eol_equence(file_obj)
        file_obj.seek(0, os.SEEK_END)
        file_obj.write(eol_seq)
        return 1

    while last_character in {b'\n', b'\r'}:
        # Deal with the beginning of the file
        if file_obj.tell() == 1:
            # If we've reached the beginning of the file and it is all
            # linebreaks then we can make this file empty
            file_obj.seek(0)
            file_obj.truncate()
            return 1

        # Go back two bytes and read a character
        file_obj.seek(-2, os.SEEK_CUR)
        last_character = file_obj.read(1)

    # Our current position is at the end of the file just before any amount of
    # newlines.  If we find extraneous newlines, then backtrack and trim them.
    position = file_obj.tell()
    remaining = file_obj.read()
    for sequence in (b'\n', b'\r\n', b'\r'):
        if remaining == sequence:
            return 0
        elif remaining.startswith(sequence):
            file_obj.seek(position + len(sequence))
            file_obj.truncate()
            return 1

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        with open(filename, 'rb+') as file_obj:
            ret_for_file = fix_file(file_obj)
            if ret_for_file:
                print(f'Fixing {filename}')
            retv |= ret_for_file

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
