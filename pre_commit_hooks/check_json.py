from __future__ import print_function

import argparse
import io
import json
import sys
from typing import Optional
from typing import Sequence


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            json.load(io.open(filename, encoding='UTF-8'))
        except (ValueError, UnicodeDecodeError) as exc:
            print('{}: Failed to json decode ({})'.format(filename, exc))
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(main())
