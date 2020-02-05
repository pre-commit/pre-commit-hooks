import argparse
import json
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        with open(filename, 'rb') as f:
            try:
                json.load(f)
            # TODO: need UnicodeDecodeError?
            except (ValueError, UnicodeDecodeError) as exc:
                print(f'{filename}: Failed to json decode ({exc})')
                retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
