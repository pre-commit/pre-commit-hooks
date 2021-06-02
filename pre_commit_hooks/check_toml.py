import argparse
from typing import Optional
from typing import Sequence

import tomli


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        with open(filename, encoding='utf-8') as f:
            try:
                tomli.load(f)
            except tomli.TOMLDecodeError as exc:
                print(f'{filename}: {exc}')
                retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
