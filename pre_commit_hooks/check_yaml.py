from __future__ import print_function

import argparse
import sys
import yaml

from pre_commit_hooks.util import entry


@entry
def check_yaml(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            yaml.load(open(filename))
        except yaml.YAMLError as e:
            print(e)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_yaml())
