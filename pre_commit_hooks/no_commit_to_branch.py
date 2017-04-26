from __future__ import print_function

import argparse
import sys

from pre_commit_hooks.util import cmd_output


def is_on_branch(protected=()):
    branch = cmd_output('git', 'symbolic-ref', 'HEAD')
    chunks = branch.strip().split('/')
    position = '/'.join(chunks[2:])
    return position in (protected or ('master',))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--branch',
        action='append',
        dest='branches',
        help='branch to disallow commits to'
    )
    args = parser.parse_args(argv)

    return int(is_on_branch(args.branches))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
