from __future__ import print_function

import argparse
import sys
import simplejson

from pre_commit_hooks.util import entry


@entry
def check_json(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='JSON filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            simplejson.load(open(filename))
        except simplejson.JSONDecodeError as e:
            print('{0}: Failed to json encode ({1})'.format(filename, e))
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_json())
