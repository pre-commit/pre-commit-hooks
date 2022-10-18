from __future__ import annotations

import argparse
import os
from typing import Sequence

from pre_commit_hooks.util import cmd_output


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--extension', choices=['yaml', 'yml'], default='yaml')
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')

    args = parser.parse_args(argv)
    extension = f'.{args.extension}'

    retval = 0
    for filename in args.filenames:
        if not filename.endswith(extension):
            new_filename = f'{os.path.splitext(filename)[0]}{extension}'
            cmd_output('git', 'mv', filename, new_filename)
            retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
