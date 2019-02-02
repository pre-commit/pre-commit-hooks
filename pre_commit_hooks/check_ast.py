from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import ast
import platform
import sys
import traceback
from typing import Optional
from typing import Sequence


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:

        try:
            with open(filename, 'rb') as f:
                ast.parse(f.read(), filename=filename)
        except SyntaxError:
            print('{}: failed parsing with {} {}:'.format(
                filename,
                platform.python_implementation(),
                sys.version.partition(' ')[0],
            ))
            print('\n{}'.format(
                '    ' + traceback.format_exc().replace('\n', '\n    '),
            ))
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
