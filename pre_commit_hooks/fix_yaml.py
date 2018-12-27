from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io

from six import text_type


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with io.open(filename, 'r+', encoding="utf-8") as f:
            line = f.readline().strip()
            if line != text_type('---'):
                print("[%s]" % line)
                f.seek(0, 0)
                content = f.read()
                f.seek(0, 0)
                f.write('---\n' + content)
                print('{}: Added --- header to YAML file'.format(filename))
                retv = 1

    return retv


if __name__ == '__main__':
    exit(main())
