"""Check that executable text files have a shebang."""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import pipes
import sys
from typing import Optional
from typing import Sequence


def check_has_shebang(path):  # type: (str) -> int
    with open(path, 'rb') as f:
        first_bytes = f.read(2)

    if first_bytes != b'#!':
        print(
            '{path}: marked executable but has no (or invalid) shebang!\n'
            "  If it isn't supposed to be executable, try: chmod -x {quoted}\n"
            '  If it is supposed to be executable, double-check its shebang.'
            .format(
                path=path,
                quoted=pipes.quote(path),
            ),
            file=sys.stderr,
        )
        return 1
    else:
        return 0


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= check_has_shebang(filename)

    return retv


if __name__ == '__main__':
    exit(main())
