from __future__ import print_function

import argparse
import fnmatch
from typing import Optional
from typing import Sequence
from typing import Set

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def is_on_branch(protected):  # type: (Set[str]) -> bool
    try:
        ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return False
    chunks = ref_name.strip().split('/')
    branch_name = '/'.join(chunks[2:])
    return any(fnmatch.fnmatch(branch_name, s) for s in protected)


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--branch', action='append',
        help='branch to disallow commits to, may be specified multiple times',
    )
    args = parser.parse_args(argv)

    protected = set(args.branch or ('master',))
    return int(is_on_branch(protected))


if __name__ == '__main__':
    exit(main())
