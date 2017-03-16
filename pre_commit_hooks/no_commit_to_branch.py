from __future__ import print_function

import argparse
import sys

import util


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', default='master', help='branch to disallow commits to')
    parser.add_argument('filenames', nargs='*', help='filenames to check.')
    args = parser.parse_args(argv)

    retval = -1
    branch = util.cmd_output('git', 'symbolic-ref', 'HEAD')
    chunks = branch.split('/')
    if chunks[2] == args.b:
        retval = 0
    return retval


if __name__ == '__main__':
    sys.exit(main())
