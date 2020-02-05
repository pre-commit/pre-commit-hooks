import argparse
from typing import Optional
from typing import Sequence

import toml


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename) as f:
                toml.load(f)
        except toml.TomlDecodeError as exc:
            print(f'{filename}: {exc}')
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
