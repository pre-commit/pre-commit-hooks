from __future__ import print_function

import argparse
import sys

import simplejson


def check_json(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='JSON filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            simplejson.load(open(filename))
        except simplejson.JSONDecodeError as exc:
            print('{0}: Failed to json encode ({1})'.format(filename, exc))
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_json())
