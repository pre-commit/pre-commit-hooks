"""
A very simple pre-commit hook that, when passed one or more filenames
as arguments, will sort the lines in those files.

An example use case for this: you have a deploy-whitelist.txt file
in a repo that contains a list of filenames that is used to specify
files to be included in a docker container. This file has one filename
per line. Various users are adding/removing lines from this file; using
this hook on that file should reduce the instances of git merge
conflicts and keep the file nicely ordered.
"""
from __future__ import print_function

import argparse
from typing import IO
from typing import Optional
from typing import Sequence

PASS = 0
FAIL = 1


def sort_file_contents(f):  # type: (IO[bytes]) -> int
    before = list(f)
    after = sorted([line.strip(b'\n\r') for line in before if line.strip()])

    before_string = b''.join(before)
    after_string = b'\n'.join(after) + b'\n'

    if before_string == after_string:
        return PASS
    else:
        f.seek(0)
        f.write(after_string)
        f.truncate()
        return FAIL


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='Files to sort')
    args = parser.parse_args(argv)

    retv = PASS

    for arg in args.filenames:
        with open(arg, 'rb+') as file_obj:
            ret_for_file = sort_file_contents(file_obj)

            if ret_for_file:
                print('Sorting {}'.format(arg))

            retv |= ret_for_file

    return retv
