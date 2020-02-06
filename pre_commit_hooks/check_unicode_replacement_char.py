import argparse
import fileinput
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0

    for line in fileinput.input(files=args.filenames, mode='rb'):
        try:
            col = line.index(b'\xEF\xBF\xBD')
        except ValueError:
            continue
        retv = 1
        # Not saying filename:line:col: because that kind of format is usually
        # used for character offsets, and we have a byte offset which might be
        # different, emphasize that.
        print(
            f'{fileinput.filename()}:{fileinput.lineno()}: '
            f'UTF-8 Unicode replacement character at byte {col}'
        )

    return retv


if __name__ == '__main__':
    exit(main())
