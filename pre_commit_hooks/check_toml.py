from __future__ import print_function

import argparse
import sys
from typing import Optional
from typing import Sequence

import pytoml


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename) as f:
                pytoml.load(f)
        except pytoml.TomlError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(main())
