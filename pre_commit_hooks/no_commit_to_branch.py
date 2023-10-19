from __future__ import annotations

import argparse
import re
from typing import AbstractSet
from typing import Sequence

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def get_current_branch() -> str | None:
    try:
        ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return None
    chunks = ref_name.strip().split('/')
    return '/'.join(chunks[2:])


def is_on_branch(
    current_branch: str,
    protected: AbstractSet[str],
    patterns: AbstractSet[str] = frozenset(),
) -> bool:
    return current_branch in protected or any(
        re.match(p, current_branch) for p in patterns
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--branch',
        action='append',
        help='branch to disallow commits to, may be specified multiple times',
    )
    parser.add_argument(
        '-p',
        '--pattern',
        action='append',
        help=(
            'regex pattern for branch name to disallow commits to, '
            'may be specified multiple times'
        ),
    )
    args = parser.parse_args(argv)

    protected = frozenset(args.branch or ('master', 'main'))
    patterns = frozenset(args.pattern or ())
    current_branch = get_current_branch()

    if current_branch is None:
        return 0

    on_branch = is_on_branch(current_branch, protected, patterns)

    if on_branch:
        print(
            f'You are currently on {current_branch} branch, for which '
            f'pre-commit script does not permit this action.',
        )

    return int(on_branch)


if __name__ == '__main__':
    raise SystemExit(main())
