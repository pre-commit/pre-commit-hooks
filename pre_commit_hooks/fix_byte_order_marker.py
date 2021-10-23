import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'rb') as f_b:
            bts = f_b.read(3)

        if bts == b'\xef\xbb\xbf':
            with open(filename, newline='', encoding='utf-8-sig') as f:
                contents = f.read()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                f.write(contents)

            print(f'{filename}: removed byte-order marker')
            retv = 1

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
