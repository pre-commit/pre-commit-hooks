from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from typing import AbstractSet

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


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
    parser.add_argument(
        '-m', '--message', default='',
        help=(
            'What message to display if the the check fails'
        ),
    )
    args = parser.parse_args(argv)

    protected = frozenset(args.branch or ('master', 'main'))
    patterns = frozenset(args.pattern or ())
    result = int(is_on_branch(protected, patterns))
    if result:
        print(args.message)
    return result


if __name__ == '__main__':
    raise SystemExit(main())
