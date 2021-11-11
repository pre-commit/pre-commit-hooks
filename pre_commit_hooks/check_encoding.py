import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    parser.add_argument('--encoding', help='Encoding to assert.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, encoding=args.encoding) as f:
                f.read()
        except LookupError as exc:
            # Unknown encoding, don't bother with the rest
            print(f'{__file__}: {exc}')
            retval = 2
            break
        except Exception as exc:
            print(f'{filename}: {exc}')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
