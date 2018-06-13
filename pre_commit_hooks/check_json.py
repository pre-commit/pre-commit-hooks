from __future__ import print_function

import argparse
import io
import json
import sys


def check_json(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='JSON filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            json.load(io.open(filename, encoding='UTF-8'))
        except (ValueError, UnicodeDecodeError) as exc:
            print('{}: Failed to json decode ({})'.format(filename, exc))
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_json())
