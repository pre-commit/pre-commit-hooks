from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys


def fix_file(file_obj):
    # Test for newline at end of file
    # Empty files will throw IOError here
    try:
        file_obj.seek(-1, os.SEEK_END)
    except IOError:
        return 0
    last_character = file_obj.read(1)
    # last_character will be '' for an empty file
    if last_character != b'\n' and last_character != b'':
        # Needs this seek for windows, otherwise IOError
        file_obj.seek(0, os.SEEK_END)
        file_obj.write(b'\n')
        return 1

    while last_character == b'\n':
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
    # newlines.  If we read two characters and get two newlines back we know
    # there are extraneous newlines at the ned of the file.  Then backtrack and
    # trim the end off.
    if len(file_obj.read(2)) == 2:
        file_obj.seek(-1, os.SEEK_CUR)
        file_obj.truncate()
        return 1

    return 0


def end_of_file_fixer(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        with open(filename, 'rb+') as file_obj:
            ret_for_file = fix_file(file_obj)
            if ret_for_file:
                print('Fixing {0}'.format(filename))
            retv |= ret_for_file

    return retv


if __name__ == '__main__':
    sys.exit(end_of_file_fixer())
