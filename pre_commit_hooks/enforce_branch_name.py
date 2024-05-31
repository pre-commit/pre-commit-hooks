from __future__ import annotations

import argparse
import re
from typing import AbstractSet
from typing import Sequence

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output

OK = 0
ERROR = 1


def branch_follows_pattern(patterns: AbstractSet[str]) -> bool:
    try:
        ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return False
    chunks = ref_name.strip().split('/')
    branch_name = '/'.join(chunks[2:])
    return any(re.match(p, branch_name) for p in patterns)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--pattern',
        action='append',
        help=('regex pattern that the name of the branch must comply with'),
    )
    args = parser.parse_args(argv)
    return OK if branch_follows_pattern(frozenset(args.pattern)) else ERROR


if __name__ == '__main__':
    raise SystemExit(main())
