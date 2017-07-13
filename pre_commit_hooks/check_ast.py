from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import ast
import platform
import sys
import traceback


def check_ast(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:

        try:
            ast.parse(open(filename, 'rb').read(), filename=filename)
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
    exit(check_ast())
