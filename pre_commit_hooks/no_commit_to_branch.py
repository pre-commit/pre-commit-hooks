from __future__ import print_function

import argparse

import util

def is_on_branch(protected):
    retval = False
    branch = util.cmd_output('git', 'symbolic-ref', 'HEAD')
    chunks = branch.strip().split('/')
    if chunks[2] == protected:
        retval = True
    return retval

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', default='master', help='branch to disallow commits to')
    parser.add_argument('filenames', nargs='*', help='filenames to check.')
    args = parser.parse_args(argv)

    if is_on_branch(args.b):
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
