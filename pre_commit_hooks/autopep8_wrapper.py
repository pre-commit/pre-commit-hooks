from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import sys

import autopep8


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = autopep8.parse_args(argv, apply_config=True)

    retv = 0
    for filename in args.files:
        original_contents = io.open(filename).read()
        new_contents = autopep8.fix_code(original_contents, args)
        if original_contents != new_contents:
            print('Fixing {0}'.format(filename))
            retv = 1
            with io.open(filename, 'w') as output_file:
                output_file.write(new_contents)

    return retv


if __name__ == '__main__':
    exit(main())
