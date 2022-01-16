from __future__ import annotations

import argparse
import ast
import platform
import sys
import traceback
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:

        try:
            with open(filename, 'rb') as f:
                ast.parse(f.read(), filename=filename)
        except SyntaxError:
            impl = platform.python_implementation()
            version = sys.version.split()[0]
            print(f'{filename}: failed parsing with {impl} {version}:')
            tb = '    ' + traceback.format_exc().replace('\n', '\n    ')
            print(f'\n{tb}')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
