from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from typing import AbstractSet

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def _default_branch() -> frozenset[str]:
    try:
        ref = cmd_output('git', 'rev-parse', '--abbrev-ref', 'origin/HEAD')
        branch = ref.strip().removeprefix('origin/')
        if branch:
            return frozenset((branch,))
    except CalledProcessError:
        pass
    return frozenset(('master', 'main'))


def is_on_branch(
        protected: AbstractSet[str],
        patterns: AbstractSet[str] = frozenset(),
) -> bool:
    try:
        ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return False
    chunks = ref_name.strip().split('/')
    branch_name = '/'.join(chunks[2:])
    return branch_name in protected or any(
        re.match(p, branch_name) for p in patterns
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--branch', action='append',
        help='branch to disallow commits to, may be specified multiple times',
    )
    parser.add_argument(
        '-p', '--pattern', action='append',
        help=(
            'regex pattern for branch name to disallow commits to, '
            'may be specified multiple times'
        ),
    )
    args = parser.parse_args(argv)

    protected = frozenset(args.branch) if args.branch else _default_branch()
    patterns = frozenset(args.pattern or ())
    return int(is_on_branch(protected, patterns))


if __name__ == '__main__':
    raise SystemExit(main())
