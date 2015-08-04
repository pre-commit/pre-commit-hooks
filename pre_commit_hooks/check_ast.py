from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import ast
import os.path
import sys
import traceback


def check_ast(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    _, interpreter = os.path.split(sys.executable)

    retval = 0
    for filename in args.filenames:

        try:
            ast.parse(open(filename, 'rb').read(), filename=filename)
        except SyntaxError:
            print('{0}: failed parsing with {1}:'.format(
                filename, interpreter,
            ))
            print('\n{0}'.format(
                '    ' + traceback.format_exc().replace('\n', '\n    ')
            ))
            retval = 1
    return retval


if __name__ == '__main__':
    exit(check_ast())
