from __future__ import annotations

import argparse
import os
from typing import Sequence

from pre_commit_hooks.util import cmd_output


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    if (
        'PRE_COMMIT_FROM_REF' in os.environ and
        'PRE_COMMIT_TO_REF' in os.environ
    ):
        diff_arg = '...'.join((
            os.environ['PRE_COMMIT_FROM_REF'],
            os.environ['PRE_COMMIT_TO_REF'],
        ))
    else:
        diff_arg = '--staged'
    added_diff = cmd_output(
        'git', 'diff', '--diff-filter=A', '--raw', diff_arg, '--',
        *args.filenames,
    )
    retv = 0
    for line in added_diff.splitlines():
        metadata, filename = line.split('\t', 1)
        new_mode = metadata.split(' ')[1]
        if new_mode == '160000':
            print(f'{filename}: new submodule introduced')
            retv = 1

    if retv:
        print()
        print('This commit introduces new submodules.')
        print('Did you unintentionally `git add .`?')
        print('To fix: git rm {thesubmodule}  # no trailing slash')
        print('Also check .gitmodules')

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
