from __future__ import annotations

import argparse
from typing import Sequence

import hcl2
# from typing import Any


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if filename == 'iam.tf':
            continue
        with open(filename, 'rb') as f:
            try:
                dict = hcl2.load(f)
            except ValueError as exc:
                print(f'{filename}: Failed to hcl decode ({exc})')
                retval = 1
        resources = data.get('resource')
        if resources:
            for item in resources:
                for keys in item:
                    if key.startswith('aws_iam'):
                        print(f'{filename}: Has {key} resource')
                        retval = 1
        resources = data.get('data')
        if resources:
            for item in resources:
                for keys in item:
                    if key.startswith('aws_iam'):
                        print(f'{filename}: Has {key} data resource')
                        retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
