from __future__ import annotations

import argparse
import re
from typing import AbstractSet
from typing import Sequence

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def has_naming_convention(
        patterns: AbstractSet[str] = frozenset(),
) -> bool:
    try:
        ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return False
    chunks = ref_name.strip().split('/')
    branch_name = '/'.join(chunks[2:])

    return any(
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
            'regex pattern for branch name to allow commits to, '
            'may be specified multiple times'
        ),
    )
    args = parser.parse_args(argv)

    patterns = frozenset(args.pattern or ())

    return int(has_naming_convention(patterns))


if __name__ == '__main__':
    raise SystemExit(main())
