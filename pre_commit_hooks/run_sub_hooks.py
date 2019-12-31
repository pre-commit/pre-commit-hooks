#!/usr/bin/env python
"""
Run pre-commit with different config under pre-commit hook.

Initial idea & code:
https://github.com/pre-commit/pre-commit/issues/731#issuecomment-376945745
"""
import argparse
import os
import subprocess
import sys
from typing import List
from typing import Optional
from typing import Sequence


def all_files(target):  # type: (str) -> List[str]
    return sum(
        (
            [os.path.join(dirpath, file) for file in filenames]
            for (dirpath, dirnames, filenames) in os.walk(target)
        ),
        [],
    )


def main(args=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--target',
        dest='target',
        help='target directory to which pre-commit should be limited',
    )
    parser.add_argument(
        '-c',
        '--config',
        dest='config',
        default='.pre-commit-config.yaml',
        help='config in relation to target directory',
    )
    parser.add_argument('--all-files', action='store_true')
    options, args = parser.parse_known_args(args)

    def is_default(arg):  # type: (str) -> bool
        return getattr(options, arg) == parser.get_default(arg)

    if is_default('target') and is_default('config'):
        parser.error('`target` or `config` has to be specified')

    precommit_cfg = os.path.join(options.target, options.config)
    cmd = ['pre-commit', 'run', '--config', precommit_cfg, '--files']

    if options.all_files:
        if options.target == '.':
            args.insert(0, '--all-files')
        else:
            args.extend(all_files(options.target))

    return subprocess.call(cmd + args, stdout=sys.stdout, stderr=sys.stderr)


if __name__ == '__main__':
    exit(main())
