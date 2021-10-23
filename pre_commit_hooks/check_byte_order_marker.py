import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            if f.read(3) == b'\xef\xbb\xbf':
                retv = 1
                print(f'{filename}: Has a byte-order marker')

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
