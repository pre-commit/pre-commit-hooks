from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import json
import math
import os
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import Set

from pre_commit_hooks.util import added_files
from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def lfs_files():  # type: () -> Set[str]
    try:
        # Introduced in git-lfs 2.2.0, first working in 2.2.1
        lfs_ret = cmd_output('git', 'lfs', 'status', '--json')
    except CalledProcessError:  # pragma: no cover (with git-lfs)
        lfs_ret = '{"files":{}}'

    return set(json.loads(lfs_ret)['files'])


def find_large_added_files(filenames, maxkb):
    # type: (Iterable[str], int) -> int
    # Find all added files that are also in the list of files pre-commit tells
    # us about
    filenames = (added_files() & set(filenames)) - lfs_files()

    retv = 0
    for filename in filenames:
        kb = int(math.ceil(os.stat(filename).st_size / 1024))
        if kb > maxkb:
            print('{} ({} KB) exceeds {} KB.'.format(filename, kb, maxkb))
            retv = 1

    return retv


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    parser.add_argument(
        '--maxkb', type=int, default=500,
        help='Maxmimum allowable KB for added files',
    )

    args = parser.parse_args(argv)
    return find_large_added_files(args.filenames, args.maxkb)


if __name__ == '__main__':
    exit(main())
