import argparse
import collections
from typing import Dict
from typing import Optional
from typing import Sequence


CRLF = b'\r\n'
LF = b'\n'
CR = b'\r'
# Prefer LF to CRLF to CR, but detect CRLF before LF
ALL_ENDINGS = (CR, CRLF, LF)
FIX_TO_LINE_ENDING = {'cr': CR, 'crlf': CRLF, 'lf': LF}


def _fix(filename: str, contents: bytes, ending: bytes) -> None:
    new_contents = b''.join(
        line.rstrip(b'\r\n') + ending for line in contents.splitlines(True)
    )
    with open(filename, 'wb') as f:
        f.write(new_contents)


def fix_filename(filename: str, fix: str) -> int:
    with open(filename, 'rb') as f:
        contents = f.read()

    counts: Dict[bytes, int] = collections.defaultdict(int)

    for line in contents.splitlines(True):
        for ending in ALL_ENDINGS:
            if line.endswith(ending):
                counts[ending] += 1
                break

    # Some amount of mixed line endings
    mixed = sum(bool(x) for x in counts.values()) > 1

    if fix == 'no' or (fix == 'auto' and not mixed):
        return mixed

    if fix == 'auto':
        # ordering is important here such that lf > crlf > cr
        # max prefers the first item when multiple items are the max
        max_ending = max(reversed(ALL_ENDINGS), key=counts.get)
        _fix(filename, contents, max_ending)
        return 1
    else:
        target_ending = FIX_TO_LINE_ENDING[fix]
        # find if there are lines with *other* endings
        # It's possible there's no line endings of the target type
        counts.pop(target_ending, None)
        other_endings = bool(sum(counts.values()))
        if other_endings:
            _fix(filename, contents, target_ending)
        return other_endings


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--fix',
        choices=('auto', 'no') + tuple(FIX_TO_LINE_ENDING),
        default='auto',
        help='Replace line ending with the specified. Default is "auto"',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        if fix_filename(filename, args.fix):
            if args.fix == 'no':
                print(f'{filename}: mixed line endings')
            else:
                print(f'{filename}: fixed mixed line endings')
            retv = 1
    return retv


if __name__ == '__main__':
    exit(main())
