from __future__ import absolute_import
from __future__ import print_function

import os.path
from argparse import ArgumentParser
from typing import Optional
from typing import Sequence
from typing import Set

OK = 0
ERR = 1


class ModuleInitChecker:
    def __init__(self):
        # type: () -> None
        self.seen_dirnames = set()  # type: Set[str]

    def check(self, filename):
        # type: (str) -> int
        dirname = os.path.dirname(filename)
        if dirname in self.seen_dirnames:
            return OK

        init_file = os.path.join(dirname, '__init__.py')
        if dirname and not os.path.exists(init_file):
            self.seen_dirnames.add(dirname)
            with open(init_file, 'w'):
                print(f'Created {init_file}')
                return ERR

        return OK


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = ArgumentParser()
    parser.add_argument('filenames', nargs='*')

    args = parser.parse_args(argv)

    status = OK
    checker = ModuleInitChecker()
    for filename in args.filenames:
        status |= checker.check(filename)

    return status


if __name__ == '__main__':
    exit(main())
