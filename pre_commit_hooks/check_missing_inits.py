import os
from argparse import ArgumentParser
from typing import Optional
from typing import Sequence


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    directories = {os.path.dirname(f) for f in args.filenames}
    missing_dirs = set()
    for d in directories:
        if not os.path.exists(os.path.join(d, '__init__.py')):
            missing_dirs.add(d)

    for d in sorted(missing_dirs):
        print('No __init__.py file found in: {}'.format(d))

    return 1 if len(missing_dirs) else 0


if __name__ == '__main__':
    exit(main())
