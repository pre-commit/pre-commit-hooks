from __future__ import print_function

import argparse
import sys

from pre_commit_hooks.util import cmd_output


def is_on_branch(protected):
    branch = cmd_output('git', 'symbolic-ref', 'HEAD')
    chunks = branch.strip().split('/')
    return '/'.join(chunks[2:]) == protected


def main(argv=[]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--branch', default='master', help='branch to disallow commits to',
    )
    args = parser.parse_args(argv)

    return int(is_on_branch(args.branch))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
