"""
Migrated from https://github.com/FalconSocial/pre-commit-python-sorter/
by @benjaoming

Thanks to FalconSocial devs for starting this.
Original author: Kasper Jacobsen, @Dinoshauer

The MIT License (MIT)

Copyright (c) 2014 Falcon Social

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os

from isort import isort


def imports_incorrect(filename, show_diff=False):
    return isort.SortImports(filename, check=True, show_diff=show_diff).incorrectly_sorted


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument('--silent-overwrite', action='store_true', dest='silent', default=False)
    parser.add_argument('--check-only', action='store_true', dest='check_only', default=False)
    parser.add_argument('--diff', action='store_true', dest='show_diff', default=False)
    args = parser.parse_args(argv)

    return_value = 0

    for filename in args.filenames:
        if imports_incorrect(filename, show_diff=args.show_diff):
            if args.check_only:
                return_value = 1
            elif args.silent:
                isort.SortImports(filename)
            else:
                return_value = 1
                isort.SortImports(filename)
                print('FIXED: {}'.format(os.path.abspath(filename)))
    return return_value


if __name__ == '__main__':
    exit(main())
