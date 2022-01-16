from __future__ import annotations

import argparse
import json
from typing import Any
from typing import Sequence


def raise_duplicate_keys(
        ordered_pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    d = {}
    for key, val in ordered_pairs:
        if key in d:
            raise ValueError(f'Duplicate key: {key}')
        else:
            d[key] = val
    return d


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        with open(filename, 'rb') as f:
            try:
                json.load(f, object_pairs_hook=raise_duplicate_keys)
            except ValueError as exc:
                print(f'{filename}: Failed to json decode ({exc})')
                retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
